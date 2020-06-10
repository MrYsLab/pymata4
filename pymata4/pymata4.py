"""
 Copyright (c) 2020 Alan Yorinks All rights reserved.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,f
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

from collections import deque
import serial
# noinspection PyPackageRequirements
from serial.tools import list_ports
# noinspection PyPackageRequirementscd
from serial.serialutil import SerialException
import socket
import sys
import threading
import time

from pymata4.pin_data import PinData
from pymata4.private_constants import PrivateConstants


# noinspection PyPep8
class Pymata4(threading.Thread):
    """
    This class exposes and implements the PymataExpress Non-asyncio API.
    It uses threading to accommodate concurrency.
    It includes the public API methods as well as
    a set of private methods.

    """

    # noinspection PyPep8,PyPep8,PyPep8
    def __init__(self, com_port=None, baud_rate=115200,
                 arduino_instance_id=1, arduino_wait=4,
                 sleep_tune=0.000001,
                 shutdown_on_exception=True, ip_address=None,
                 ip_port=None):
        """
        If you are using the Firmata Express Arduino sketch,
        and have a single Arduino connected to your computer,
        then you may accept all the default values.

        If you are using some other Firmata sketch, then
        you must specify both the com_port and baudrate for
        as serial connection, or ip_address and ip_port if
        using StandardFirmataWifi.

        :param com_port: e.g. COM3 or /dev/ttyACM0.

        :param baud_rate: Match this to the Firmata sketch in use.

        :param arduino_instance_id: If you are using the Firmata
                                    Express sketch, match this
                                    value to that in the sketch.

        :param arduino_wait: Amount of time to wait for an Arduino to
                             fully reset itself.

        :param sleep_tune: A tuning parameter (typically not changed by user)

        :param shutdown_on_exception: call shutdown before raising
                                      a RunTimeError exception, or
                                      receiving a KeyboardInterrupt exception

        :param ip_address: Used with StandardFirmataWifi to specify IP address of
                           the WiFi device

        :param ip_port: Used with StandardFirmataWifi to specify IP port of
                           the WiFi device. Typically this is 3030

        """
        self.start_time = time.time()
        # initialize threading parent
        threading.Thread.__init__(self)

        # create the threads and set them as daemons so
        # that they stop when the program is closed

        # create a thread to interpret received serial data
        self.the_reporter_thread = threading.Thread(target=self._reporter)
        self.the_reporter_thread.daemon = True

        self.ip_address = ip_address
        self.ip_port = ip_port

        # if an ip address was specified, tcp/ip will be used instead of serial
        # transfer.
        # create a thread to continuously receive data
        if self.ip_address:
            self.the_data_receive_thread = threading.Thread(target=self._tcp_receiver)
        else:
            self.the_data_receive_thread = threading.Thread(target=self._serial_receiver)

        self.the_data_receive_thread.daemon = True

        # keep alive variables
        self.keep_alive_interval = []
        self.period = 0
        self.margin = 0

        # create a thread for the keep alives
        self.the_keep_alive_thread = threading.Thread(target=self._send_keep_alive)
        self.the_keep_alive_thread.daemon = True

        # flag to allow the reporter and receive threads to run.
        self.run_event = threading.Event()

        # check to make sure that Python interpreter is version 3.7 or greater
        python_version = sys.version_info
        if python_version[0] >= 3:
            if python_version[1] >= 7:
                pass
            else:
                raise RuntimeError("ERROR: Python 3.7 or greater is "
                                   "required for use of this program.")

        # save input parameters as instance variables
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.arduino_instance_id = arduino_instance_id
        self.arduino_wait = arduino_wait
        self.sleep_tune = sleep_tune
        self.shutdown_on_exception = shutdown_on_exception

        # create a deque to receive and process data from the arduino
        self.the_deque = deque()

        # The report_dispatch dictionary is used to process
        # incoming report sysex message by looking up the sysex command
        # and executing its associated processing method.
        # The value following the method is the number of bytes to
        # retrieve from the deque to process the command.
        self.report_dispatch = {}

        # To add a command to the command dispatch table, append here.
        self.report_dispatch.update({PrivateConstants.REPORT_VERSION: [self._report_version, 2]})
        self.report_dispatch.update({PrivateConstants.REPORT_FIRMWARE: [self._report_firmware, 1]})
        self.report_dispatch.update({PrivateConstants.ANALOG_MESSAGE: [self._analog_message, 2]})
        self.report_dispatch.update({PrivateConstants.DIGITAL_MESSAGE: [self._digital_message, 2]})
        self.report_dispatch.update({PrivateConstants.SONAR_DATA: [self._sonar_data, 3]})
        self.report_dispatch.update({PrivateConstants.STRING_DATA: [self._string_data, 2]})
        self.report_dispatch.update({PrivateConstants.I2C_REPLY: [self._i2c_reply, 2]})
        self.report_dispatch.update({PrivateConstants.CAPABILITY_RESPONSE: [self._capability_response, 2]})
        self.report_dispatch.update({PrivateConstants.PIN_STATE_RESPONSE: [self._pin_state_response, 2]})
        self.report_dispatch.update({PrivateConstants.ANALOG_MAPPING_RESPONSE: [self._analog_mapping_response, 4]})
        self.report_dispatch.update({PrivateConstants.DHT_DATA: [self._dht_read_response, 7]})

        # report query results are stored in this dictionary
        self.query_reply_data = {PrivateConstants.REPORT_VERSION: '',
                                 PrivateConstants.STRING_DATA: '',
                                 PrivateConstants.REPORT_FIRMWARE: '',
                                 PrivateConstants.CAPABILITY_RESPONSE: None,
                                 PrivateConstants.ANALOG_MAPPING_RESPONSE:
                                     None,
                                 PrivateConstants.PIN_STATE_RESPONSE: None}

        self.firmata_firmware = []

        # a flag to indicate if using FirmataExpress
        self.using_firmata_express = False

        # dht error flag
        self.dht_sensor_error = False

        # a list of PinData objects - one for each pin segregated by pin type
        # see pin_data.py
        self.analog_pins = []
        self.digital_pins = []

        # a list of pins assigned to DHT devices
        self.dht_list = []

        # This lock is used when the PinData object is update or contents
        # are retrieved
        self.the_pin_data_lock = threading.Lock()

        # a lock for the i2c map data structure
        self.the_i2c_map_lock = threading.Lock()

        # a lock for the sonar map
        self.the_sonar_map_lock = threading.Lock()

        # a when sending data to the arduino
        self.the_send_sysex_lock = threading.Lock()

        # serial port in use
        self.serial_port = None

        # handle to tcp/ip socket
        self.sock = None

        # An i2c_map entry consists of a device i2c address as the key, and
        #  the value of the key consists of a dictionary containing 2 entries.
        #  The first entry. 'value' contains the last value reported, and
        # the second, 'callback' contains a reference to a callback function,
        # and the third, a time-stamp
        # For example:
        # {12345: {'value': 23, 'callback': None, time_stamp:None}}
        self.i2c_map = {}

        # The active_sonar_map maps the sonar trigger pin number (the key)
        # to the current data value returned
        # if a callback was specified, it is stored in the map as well.
        # A map entry consists of:
        #   pin: [callback, current_data_returned, time_stamp]
        self.active_sonar_map = {}

        # first analog pin number
        self.first_analog_pin = None

        # flag to indicate we are in shutdown mode
        self.shutdown_flag = False

        print(f"pymata4:  Version {PrivateConstants.PYMATA_EXPRESS_THREADED_VERSION}\n\n"
              f"Copyright (c) 2020 Alan Yorinks All Rights Reserved.\n")
        # if this is not a tcp interface, find the serial port
        if not self.ip_address:
            if not self.com_port:
                # user did not specify a com_port
                try:
                    self._find_arduino()
                except KeyboardInterrupt:
                    if self.shutdown_on_exception:
                        self.shutdown()
            else:
                # com_port specified - set com_port and baud rate
                try:
                    self._manual_open()
                except KeyboardInterrupt:
                    if self.shutdown_on_exception:
                        self.shutdown()

            if self.serial_port:
                print(f"Arduino compatible device found and connected to {self.serial_port.port}")

            # no com_port found - raise a runtime exception
            else:
                if self.shutdown_on_exception:
                    self.shutdown()
                raise RuntimeError('No Arduino Found or User Aborted Program')
        # this is tcp/ip interface
        else:
            # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.sock:
            #     s = self.sock.create_connection((self.ip_address, self.ip_port))
            #     print(s)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.ip_address, self.ip_port))
            print(f'Successfully connected to: {self.ip_address}:{self.ip_port}')

        self.the_reporter_thread.start()
        self.the_data_receive_thread.start()

        # allow the threads to run
        self._run_threads()

        # get arduino firmware version and print it
        try:
            print('\nRetrieving Arduino Firmware ID...')
            firmware_version = self.get_firmware_version()

            if not firmware_version:
                if self.shutdown_on_exception:
                    self.shutdown()
                raise RuntimeError(f'Firmata Sketch Firmware Version Not Found')
            else:
                if self.using_firmata_express:
                    version_number = firmware_version[0:3]
                    if version_number != PrivateConstants.FIRMATA_EXPRESS_VERSION:
                        raise RuntimeError(f'You must use FirmataExpress version 1.1. Version Found = {version_number}')
                print(f'Arduino Firmware ID: {firmware_version}')
        except TypeError:
            print('\nIs your serial cable plugged in and do you have the '
                  'correct Firmata sketch loaded?')
            print('Is the COM port correct?')
            print('To see a list of serial ports, type: "list_serial_ports" '
                  'in your console.')
            raise RuntimeError
        except KeyboardInterrupt:
            if self.shutdown_on_exception:
                self.shutdown()
            raise RuntimeError('No Arduino Found or User Aborted Program')

        print('\nRetrieving analog map...')

        # try to get an analog pin map. if it comes back as none raise an exception

        report = self.get_analog_map()
        if not report:
            if self.shutdown_on_exception:
                self.shutdown()
            raise RuntimeError(f'*** Analog map retrieval timed out. ***'
                               f'\nDo you have Arduino connectivity and do you have the '
                               f'correct Firmata sketch uploaded to the board?')

        # custom assemble the pin lists
        try:
            for pin in report:
                digital_data = PinData(self.the_pin_data_lock)
                self.digital_pins.append(digital_data)
                if pin != PrivateConstants.IGNORE:
                    analog_data = PinData(self.the_pin_data_lock)
                    self.analog_pins.append(analog_data)

            print(f'Auto-discovery complete. Found {len(self.digital_pins)} Digital Pins'
                  f' and {len(self.analog_pins)} Analog Pins\n\n')
            self.first_analog_pin = len(self.digital_pins) - len(self.analog_pins)
        except KeyboardInterrupt:
            if self.shutdown_on_exception:
                self.shutdown()
            raise RuntimeError('User Hit Control-C')

        # Set the sampling interval to the standard value
        # so the the DHT and HC-SRO4 device report at the right
        # time frame.
        self.set_sampling_interval(19)

    def _find_arduino(self):
        """
        This method will search all potential serial ports for an Arduino
        containing a sketch that has a matching arduino_instance_id as
        specified in the input parameters of this class.

        This is used explicitly with the FirmataExpress sketch.
        """

        # a list of serial ports to be checked
        serial_ports = []

        print('Opening all potential serial ports...')
        the_ports_list = list_ports.comports()
        for port in the_ports_list:
            if port.pid is None:
                continue
            try:
                self.serial_port = serial.Serial(port.device, self.baud_rate,
                                                 timeout=1, writeTimeout=0)
            except SerialException:
                continue
            # create a list of serial ports that we opened
            serial_ports.append(self.serial_port)

            # display to the user
            print('\t' + port.device)

            # clear out any possible data in the input buffer
            self.serial_port.reset_input_buffer()
            self.serial_port.reset_output_buffer()

        # wait for arduino to reset
        print(f'\nWaiting {self.arduino_wait} seconds(arduino_wait) for Arduino devices to '
              'reset...')
        try:
            time.sleep(self.arduino_wait)

            print(f'\nSearching for an Arduino configured with an arduino_instance = {self.arduino_instance_id}')

            for serial_port in serial_ports:
                self.serial_port = serial_port
                # send the "are you there" sysex request to the arduino
                self._send_sysex(PrivateConstants.ARE_YOU_THERE)

                # wait until the END_SYSEX comes back
                i_am_here = self.serial_port.read_until(b'\xf7')
                if not i_am_here:
                    continue

                # make sure we get back the expected length
                if len(i_am_here) != 4:
                    continue

                # convert i_am_here to a list
                i_am_here = list(i_am_here)

                # check sysex command is I_AM_HERE
                if i_am_here[1] != PrivateConstants.I_AM_HERE:
                    continue
                else:
                    # got an I am here message - is it the correct ID?
                    if i_am_here[2] == self.arduino_instance_id:
                        self.using_firmata_express = True
                        self.com_port = self.serial_port
        except KeyboardInterrupt:
            raise RuntimeError('User Hit Control-C')

    def _manual_open(self):
        """
        Com port was specified by the user - try to open up that port

        """
        # if port is not found, a serial exception will be thrown
        try:
            print(f'Opening {self.com_port}...')
            self.serial_port = serial.Serial(self.com_port, self.baud_rate,
                                             timeout=1, writeTimeout=0)

            print(f'\nWaiting {self.arduino_wait} seconds(arduino_wait) for Arduino devices to '
                  'reset...')
            time.sleep(self.arduino_wait)
            # time.sleep(self.arduino_wait)
            if self.baud_rate == 115200:
                self._send_sysex(PrivateConstants.ARE_YOU_THERE)

                # wait until the END_SYSEX comes back
                i_am_here = self.serial_port.read_until(b'\xf7')

                # convert i_am_here to a list
                i_am_here = list(i_am_here)

                if len(i_am_here) != 4:
                    raise RuntimeError('Invalid Arduino ID reply length')

                # check sysex command is I_AM_HERE
                if i_am_here[1] != PrivateConstants.I_AM_HERE:
                    raise RuntimeError('Retrieving ID From Arduino Failed.')
                else:
                    # got an I am here message - is it the correct ID?
                    if i_am_here[2] == self.arduino_instance_id:
                        return
                    else:
                        raise RuntimeError('Invalid Arduino identifier retrieved')
        except KeyboardInterrupt:
            raise RuntimeError('User Hit Control-C')

    def analog_read(self, pin):
        """
        Retrieve the last data update for the specified analog pin.

        :param pin: Analog pin number (ex. A2 is specified as 2)

        :returns: A list = [last value change,  time_stamp]
        """
        return self.analog_pins[pin].current_value, self.analog_pins[pin].event_time

    def dht_read(self, pin):
        """
        Retrieve the last data update for the specified dht pin.

        :param pin: digital pin number

        :return: A list = [humidity, temperature  time_stamp]

                 ERROR CODES: If either humidity or temperature value:
                              == -1 Configuration Error
                              == -2 Checksum Error
                              == -3 Timeout Error

        """
        return self.digital_pins[pin].current_value[0], \
               self.digital_pins[pin].current_value[1], \
               self.digital_pins[pin].event_time

    def digital_read(self, pin):
        """
        Retrieve the last data update for the specified digital pin.

        :param pin: Digital pin number

        :returns: A list = [last value change,  time_stamp]

        """
        return [self.digital_pins[pin].current_value, self.digital_pins[pin].event_time]

    def digital_pin_write(self, pin, value):
        """
        Set the specified pin to the specified value directly without port manipulation.

        :param pin: arduino pin number

        :param value: pin value

        """

        command = (PrivateConstants.SET_DIGITAL_PIN_VALUE, pin, value)

        self._send_command(command)

    def digital_write(self, pin, value):
        """
        Set the specified pin to the specified value.

        :param pin: arduino pin number

        :param value: pin value (1 or 0)

        """
        # The command value is not a fixed value, but needs to be calculated
        # using the pin's port number
        port = pin // 8

        calculated_command = PrivateConstants.DIGITAL_MESSAGE + port
        mask = 1 << (pin % 8)
        # Calculate the value for the pin's position in the port mask
        if value == 1:
            PrivateConstants.DIGITAL_OUTPUT_PORT_PINS[port] |= mask
        else:
            PrivateConstants.DIGITAL_OUTPUT_PORT_PINS[port] &= ~mask

        # Assemble the command
        command = (calculated_command,
                   PrivateConstants.DIGITAL_OUTPUT_PORT_PINS[port] & 0x7f,
                   (PrivateConstants.DIGITAL_OUTPUT_PORT_PINS[port] >> 7)
                   & 0x7f)

        self._send_command(command)

    def disable_analog_reporting(self, pin):
        """
        Disables analog reporting for a single analog pin.

        :param pin: Analog pin number. For example for A0, the number is 0.

        """
        pin = pin + self.first_analog_pin
        self.set_pin_mode_digital_input(pin)

    def disable_digital_reporting(self, pin):
        """
        Disables digital reporting. By turning reporting off for this pin,
        Reporting is disabled for all 8 bits in the "port"

        :param pin: Pin and all pins for this port

        """
        port = pin // 8
        command = [PrivateConstants.REPORT_DIGITAL + port,
                   PrivateConstants.REPORTING_DISABLE]
        self._send_command(command)

    def enable_analog_reporting(self, pin, callback=None, differential=1):
        """
        Enables analog reporting. This is an alias for set_pin_mode_analog_input.
        Disabling analog reporting sets the pin to a digital input pin,
        so we need to provide the callback and differential if we wish
        to specify it.

        :param pin: Analog pin number. For example for A0, the number is 0.

        :param callback: callback function

        :param differential: This value needs to be met for a callback
                             to be invoked.
        """
        self.set_pin_mode_analog_input(pin, callback, differential)

    def enable_digital_reporting(self, pin):
        """
        Enables digital reporting. By turning reporting on for all 8 bits
        in the "port" - this is part of Firmata's protocol specification.

        :param pin: Pin and all pins for this port

        :returns: No return value
            """
        port = pin // 8
        command = [PrivateConstants.REPORT_DIGITAL + port,
                   PrivateConstants.REPORTING_ENABLE]
        self._send_command(command)

    def get_analog_map(self):
        """
        This method requests a Firmata analog map query and returns the
        results.

        :returns: An analog map response or None if a timeout occurs
        """
        # get the current time to make sure a report is retrieved
        current_time = time.time()

        # if we do not have existing report results, send a Firmata
        # message to request one

        self._send_sysex(PrivateConstants.ANALOG_MAPPING_QUERY)
        # wait for the report results to return for 4 seconds
        # if the timer expires, return None
        while self.query_reply_data.get(
                PrivateConstants.ANALOG_MAPPING_RESPONSE) is None:
            elapsed_time = time.time()
            if elapsed_time - current_time > 4:
                return None
            # time.sleep(self.sleep_tune)
            time.sleep(.01)
        return self.query_reply_data.get(PrivateConstants.ANALOG_MAPPING_RESPONSE)

    def get_capability_report(self):
        """
        This method requests and returns a Firmata capability query report

        :returns: A capability report in the form of a list
        """

        self._send_sysex(PrivateConstants.CAPABILITY_QUERY)
        while self.query_reply_data.get(
                PrivateConstants.CAPABILITY_RESPONSE) is None:
            time.sleep(self.sleep_tune)
        return self.query_reply_data.get(PrivateConstants.CAPABILITY_RESPONSE)

    def get_firmware_version(self):
        """
        This method retrieves the Firmata firmware version

        :returns: Firmata firmware version
        """
        self._send_sysex(PrivateConstants.REPORT_FIRMWARE)

        current_time = time.time()
        while self.query_reply_data.get(PrivateConstants.REPORT_FIRMWARE) == '':
            elapsed_time = time.time()
            if elapsed_time - current_time > 4:
                return None
            time.sleep(self.sleep_tune)
        return self.query_reply_data.get(PrivateConstants.REPORT_FIRMWARE)

    def get_protocol_version(self):
        """
        This method returns the major and minor values for the protocol
        version, i.e. 2.5

        :returns: Firmata protocol version
        """
        self._send_command([PrivateConstants.REPORT_VERSION])
        while self.query_reply_data.get(
                PrivateConstants.REPORT_VERSION) == '':
            time.sleep(self.sleep_tune)
        # v_major =
        return self.query_reply_data.get(PrivateConstants.REPORT_VERSION)

    def get_pin_state(self, pin):
        """
        This method retrieves a pin state report for the specified pin.
        Pin modes reported:

        INPUT   = 0x00  # digital input mode

        OUTPUT  = 0x01  # digital output mode

        ANALOG  = 0x02  # analog input mode

        PWM     = 0x03  # digital pin in PWM output mode

        SERVO   = 0x04  # digital pin in Servo output mode

        I2C     = 0x06  # pin included in I2C setup

        STEPPER = 0x08  # digital pin in stepper mode

        PULLUP  = 0x0b  # digital pin in input pullup mode

        SONAR   = 0x0c  # digital pin in SONAR mode

        TONE    = 0x0d  # digital pin in tone mode

        :param pin: Pin of interest

        :returns: pin state report

        """
        # place pin in a list to keep _send_sysex happy
        self._send_sysex(PrivateConstants.PIN_STATE_QUERY, [pin])
        while self.query_reply_data.get(
                PrivateConstants.PIN_STATE_RESPONSE) is None:
            time.sleep(self.sleep_tune)
        pin_state_report = self.query_reply_data.get(
            PrivateConstants.PIN_STATE_RESPONSE)
        self.query_reply_data[PrivateConstants.PIN_STATE_RESPONSE] = None
        return pin_state_report

    # noinspection PyMethodMayBeStatic
    def get_pymata_version(self):
        """
        This method retrieves the PyMata Express version number

        :returns: PyMata Express version number.
        """
        return PrivateConstants.PYMATA_EXPRESS_THREADED_VERSION

    def i2c_read_saved_data(self, address):
        """
        This method retrieves cached i2c data to support a polling mode.

        :param address: I2C device address

        :returns data: [raw data returned from i2c device, time-stamp]

        """
        if address in self.i2c_map:
            with self.the_i2c_map_lock:
                map_entry = self.i2c_map.get(address)
                return map_entry.get('value')
        else:
            return None

    def i2c_read(self, address, register, number_of_bytes,
                 callback=None):
        """
        Read the specified number of bytes from the specified register for
        the i2c device.


        :param address: i2c device address

        :param register: i2c register (or None if no register selection is needed)

        :param number_of_bytes: number of bytes to be read

        :param callback: Optional callback function to report i2c data as a
                   result of read command


        callback returns a data list:

        [pin_type, i2c_device_address, i2c_read_register, data_bytes returned, time_stamp]

        The pin_type for i2c = 6

        """

        self._i2c_read_request(address, register, number_of_bytes,
                               PrivateConstants.I2C_READ, callback)

    def i2c_read_continuous(self, address, register, number_of_bytes,
                            callback=None):
        """
        Some i2c devices support a continuous streaming data output.
        This command enables that mode for the device that supports
        continuous reads.


        :param address: i2c device address

        :param register: i2c register (or None if no register selection is needed)

        :param number_of_bytes: number of bytes to be read

        :param callback: Optional callback function to report i2c data as a
                   result of read command


        callback returns a data list:

        [pin_type, i2c_device_address, i2c_read_register, data_bytes returned, time_stamp]

        The pin_type for i2c = 6


        """

        self._i2c_read_request(address, register, number_of_bytes,
                               PrivateConstants.I2C_READ_CONTINUOUSLY,
                               callback)

    def i2c_read_restart_transmission(self, address, register,
                                      number_of_bytes,
                                      callback=None):
        """
        Read the specified number of bytes from the specified register for
        the i2c device. This restarts the transmission after the read. It is
        required for some i2c devices such as the MMA8452Q accelerometer.


        :param address: i2c device address

        :param register: i2c register

        :param number_of_bytes: number of bytes to be read

        :param callback: Optional callback function to report i2c data as a
                   result of read command


        callback returns a data list:

        [pin_type, i2c_device_address, i2c_read_register, data_bytes returned, time_stamp]

        The pin_type for i2c pins = 6

        """

        self._i2c_read_request(address, register, number_of_bytes,
                               PrivateConstants.I2C_READ
                               | PrivateConstants.I2C_END_TX_MASK,
                               callback)

    def _i2c_read_request(self, address, register, number_of_bytes, read_type,
                          callback=None):
        """
        This method requests the read of an i2c device. Results are retrieved
        by a call to i2c_get_read_data(). or by callback.

        If a callback method is provided, when data is received from the
        device it will be sent to the callback method.

        Some devices require that transmission be restarted
        (e.g. MMA8452Q accelerometer).

        I2C_READ | I2C_END_TX_MASK values for the read_type in those cases.

        I2C_READ = 0B00001000

        I2C_READ_CONTINUOUSLY = 0B00010000

        I2C_STOP_READING = 0B00011000

        I2C_END_TX_MASK = 0B01000000

        :param address: i2c device address

        :param register: register number (or None if no register selection is needed)

        :param number_of_bytes: number of bytes expected to be returned

        :param read_type: I2C_READ  or I2C_READ_CONTINUOUSLY. I2C_END_TX_MASK
                          may be OR'ed when required

        :param callback: Optional callback function to report i2c data as a
                   result of read command

        """
        if address not in self.i2c_map:
            with self.the_i2c_map_lock:
                self.i2c_map[address] = {'value': None, 'callback': callback}
        if register is not None:
            data = [address, read_type, register & 0x7f, (register >> 7) & 0x7f,
                    number_of_bytes & 0x7f, (number_of_bytes >> 7) & 0x7f]
        else:
            data = [address, read_type, 
                    number_of_bytes & 0x7f, (number_of_bytes >> 7) & 0x7f]
        self._send_sysex(PrivateConstants.I2C_REQUEST, data)

    def i2c_write(self, address, args):
        """
        Write data to an i2c device.

        :param address: i2c device address

        :param args: A variable number of bytes to be sent to the device
                     passed in as a list

        """
        data = [address, PrivateConstants.I2C_WRITE]
        for item in args:
            item_lsb = item & 0x7f
            data.append(item_lsb)
            item_msb = (item >> 7) & 0x7f
            data.append(item_msb)
        self._send_sysex(PrivateConstants.I2C_REQUEST, data)

    def keep_alive(self, period=1, margin=.3):
        """
        This is a FirmataExpress feature.

        Periodically send a keep alive message to the Arduino.

        If the Arduino does not received a keep alive, the Arduino
        will physically reset itself.

        Frequency of keep alive transmission is calculated as follows:
        keep_alive_sent = period - margin

        :param period: Time period between keepalives. Range is 0-10 seconds.
                       0 disables the keepalive mechanism.

        :param margin: Safety margin to assure keepalives are sent before
                    period expires. Range is 0.1 to 0.9
        """
        if period < 0:
            period = 0
        if period > 10:
            period = 10
        self.period = period
        if margin < .1:
            margin = .1
        if margin > .9:
            margin = .9
        self.margin = margin
        self.period = period
        self.keep_alive_interval = [self.period & 0x7f, (self.period >> 7) & 0x7f]
        self._send_sysex(PrivateConstants.SAMPLING_INTERVAL,
                         self.keep_alive_interval)
        self.the_keep_alive_thread.start()

    def play_tone(self, pin_number, frequency, duration):
        """

        This is FirmataExpress feature

        Play a tone at the specified frequency for the specified duration.

        :param pin_number: arduino pin number

        :param frequency: tone frequency in hz

        :param duration: duration in milliseconds

        """
        self._play_tone(pin_number, PrivateConstants.TONE_TONE, frequency=frequency,
                        duration=duration)

    def play_tone_continuously(self, pin_number, frequency):
        """

        This is a FirmataExpress feature

        This method plays a tone continuously until play_tone_off is called.

        :param pin_number: arduino pin number

        :param frequency: tone frequency in hz

        """

        self._play_tone(pin_number, PrivateConstants.TONE_TONE, frequency=frequency,
                        duration=None)

    def play_tone_off(self, pin_number):
        """
        This is a FirmataExpress Feature

        This method turns tone off for the specified pin.
        :param pin_number: arduino pin number

        """

        self._play_tone(pin_number, PrivateConstants.TONE_NO_TONE,
                        frequency=None, duration=None)

    def _play_tone(self, pin, tone_command, frequency, duration):
        """
        This method will call the Tone library for the selected pin.
        It requires FirmataExpress to be loaded onto the arduino

        If the tone command is set to TONE_TONE, then the specified
        tone will be played.

        Else, if the tone command is TONE_NO_TONE, then any currently
        playing tone will be disabled.

        :param pin: arduino pin number

        :param tone_command: Either TONE_TONE, or TONE_NO_TONE

        :param frequency: Frequency of tone

        :param duration: Duration of tone in milliseconds

        """
        # convert the integer values to bytes
        if tone_command == PrivateConstants.TONE_TONE:
            # duration is specified
            if duration:
                data = [tone_command, pin, frequency & 0x7f,
                        (frequency >> 7) & 0x7f,
                        duration & 0x7f, (duration >> 7) & 0x7f]

            else:
                data = [tone_command, pin,
                        frequency & 0x7f, (frequency >> 7) & 0x7f, 0, 0]
        # turn off tone
        else:
            data = [tone_command, pin]
        self._send_sysex(PrivateConstants.TONE_DATA, data)

    def pwm_write(self, pin, value):
        """
        Set the selected pwm pin to the specified value.

        :param pin: PWM pin number

        :param value: Pin value (0 - 0x4000)

        """
        if PrivateConstants.PWM_MESSAGE + pin < 0xf0:
            command = [PrivateConstants.PWM_MESSAGE + pin, value & 0x7f,
                       (value >> 7) & 0x7f]
            self._send_command(command)
        else:
            self._pwm_write_extended(pin, value)

    def _pwm_write_extended(self, pin, data):
        """
        This method will send an extended-data analog write command to the
        selected pin.

        :param pin: 0 - 127

        :param data: 0 - 0xfffff

        :returns: No return value
        """
        pwm_data = [pin, data & 0x7f, (data >> 7) & 0x7f,
                    (data >> 14) & 0x7f]
        self._send_sysex(PrivateConstants.EXTENDED_PWM, pwm_data)

    def send_reset(self):
        """
        Send a Sysex reset command to the arduino

        """
        try:
            self._send_command([PrivateConstants.SYSTEM_RESET])
        except RuntimeError:
            raise

    def set_pin_mode_analog_input(self, pin_number, callback=None,
                                  differential=1):
        """
        Set a pin as an analog input.

        :param pin_number: arduino pin number

        :param callback: callback function

        :param differential: This value needs to be met for a callback
                             to be invoked.


        callback returns a data list:

        [pin_type, pin_number, pin_value, raw_time_stamp]

        The pin_type for analog input pins = 2

        """
        self._set_pin_mode(pin_number, PrivateConstants.ANALOG,
                           callback=callback,
                           differential=differential)

    def set_pin_mode_dht(self, pin_number, sensor_type=22, differential=.1, callback=None):
        """
        Configure a DHT sensor prior to operation.
        Up to 6 DHT sensors are supported

        :param pin_number: digital pin number on arduino.

        :param sensor_type: type of dht sensor
                            Valid values = DHT11, DHT12, DHT22, DHT21, AM2301

        :param differential: This value needs to be met for a callback
                             to be invoked.

        :param callback: callback function

        callback: returns a data list:

        [pin_type, pin_number, DHT type, humidity value, temperature raw_time_stamp]

        The pin_type for DHT input pins = 15

                ERROR CODES: If either humidity or temperature value:
                              == -1 Configuration Error
                              == -2 Checksum Error
                              == -3 Timeout Error
        """

        # if the pin is not currently associated with a DHT device
        # initialize it.
        if pin_number not in self.dht_list:
            self.dht_list.append(pin_number)
            self.digital_pins[pin_number].cb = callback
            self.digital_pins[pin_number].current_value = [0, 0]
            self.digital_pins[pin_number].differential = differential
            data = [pin_number, sensor_type]
            self._send_sysex(PrivateConstants.DHT_CONFIG, data)
        else:
            # allow user to change the differential value
            self.digital_pins[pin_number].differential = differential

    def set_pin_mode_digital_input(self, pin_number, callback=None):
        """
        Set a pin as a digital input.

        :param pin_number: arduino pin number

        :param callback: callback function


        callback returns a data list:

        [pin_type, pin_number, pin_value, raw_time_stamp]

        The pin_type for digital input pins = 0

        """
        self._set_pin_mode(pin_number, PrivateConstants.INPUT, callback)

    def set_pin_mode_digital_input_pullup(self, pin_number, callback=None):
        """
        Set a pin as a digital input with pullup enabled.

        :param pin_number: arduino pin number

        :param callback: callback function


        callback returns a data list:

        [pin_type, pin_number, pin_value, raw_time_stamp]

        The pin_type for digital input pins with pullups enabled = 11

        """
        self._set_pin_mode(pin_number, PrivateConstants.PULLUP, callback)

    def set_pin_mode_digital_output(self, pin_number):
        """
        Set a pin as a digital output pin.

        :param pin_number: arduino pin number
        """

        self._set_pin_mode(pin_number, PrivateConstants.OUTPUT)

    # noinspection PyIncorrectDocstring
    def set_pin_mode_i2c(self, read_delay_time=0):
        """
        Establish the standard Arduino i2c pins for i2c utilization.

        NOTE: THIS METHOD MUST BE CALLED BEFORE ANY I2C REQUEST IS MADE
        This method initializes Firmata for I2c operations.

        :param read_delay_time (in microseconds): an optional parameter,
                                                  default is 0

        NOTE: Callbacks are set within the individual i2c read methods of this
              API.
              See i2c_read, i2c_read_continuous, or i2c_read_restart_transmission.

        """
        data = [read_delay_time & 0x7f, (read_delay_time >> 7) & 0x7f]
        self._send_sysex(PrivateConstants.I2C_CONFIG, data)

    def set_pin_mode_pwm_output(self, pin_number):
        """
        Set a pin as a pwm (analog output) pin.

        :param pin_number:arduino pin number

        """
        self._set_pin_mode(pin_number, PrivateConstants.PWM)

    def set_pin_mode_servo(self, pin, min_pulse=544, max_pulse=2400):
        """
        Configure a pin as a servo pin. Set pulse min, max in ms.

        :param pin: Servo Pin.

        :param min_pulse: Min pulse width in ms.

        :param max_pulse: Max pulse width in ms.

        """
        command = [pin, min_pulse & 0x7f, (min_pulse >> 7) & 0x7f,
                   max_pulse & 0x7f,
                   (max_pulse >> 7) & 0x7f]

        self._send_sysex(PrivateConstants.SERVO_CONFIG, command)

    def set_pin_mode_sonar(self, trigger_pin, echo_pin,
                           callback=None, timeout=80000):
        """
        This is a FirmataExpress feature.

        Configure the pins,ping interval and maximum distance for an HC-SR04
        type device.

        Up to a maximum of 6 SONAR devices is supported.
        If the maximum is exceeded a message is sent to the console and the
        request is ignored.

        NOTE: data is measured in centimeters. Callback is called only when the
              the latest value received is different than the previous.

        :param trigger_pin: The pin number of for the trigger (transmitter).

        :param echo_pin: The pin number for the received echo.

        :param callback: optional callback function to report sonar data changes

        :param timeout: a tuning parameter. 80000UL equals 80ms.


        callback returns a data list:

        [pin_type, trigger_pin_number, distance_value (in cm), raw_time_stamp]

        The pin_type for sonar pins = 12


        """
        # if there is an entry for the trigger pin in existence,
        # ignore the duplicate request.
        if trigger_pin in self.active_sonar_map:
            return

        timeout_lsb = timeout & 0x7f
        timeout_msb = (timeout >> 7) & 0x7f
        data = [trigger_pin, echo_pin, timeout_lsb,
                timeout_msb]

        self._set_pin_mode(trigger_pin, PrivateConstants.SONAR,
                           PrivateConstants.INPUT)
        self._set_pin_mode(echo_pin, PrivateConstants.SONAR,
                           PrivateConstants.INPUT)
        # update the ping data map for this pin
        if len(self.active_sonar_map) > 6:
            print('sonar_config: maximum number of devices assigned'
                  ' - ignoring request')
        else:
            # initialize map entry with callback, data value of 0 and time_stamp of 0
            self.active_sonar_map[trigger_pin] = [callback, 0, 0]

        self._send_sysex(PrivateConstants.SONAR_CONFIG, data)

    def set_pin_mode_stepper(self, steps_per_revolution, stepper_pins):
        """
        This is a FirmataExpress feature.

        Configure stepper motor prior to operation.

        NOTE: Single stepper only. Multiple steppers not supported.

        :param steps_per_revolution: number of steps per motor revolution

        :param stepper_pins: a list of control pin numbers - either 4 or 2

        """
        data = [PrivateConstants.STEPPER_CONFIGURE,
                steps_per_revolution & 0x7f,
                (steps_per_revolution >> 7) & 0x7f]
        for pin in range(len(stepper_pins)):
            data.append(stepper_pins[pin])
        self._send_sysex(PrivateConstants.STEPPER_DATA, data)

    def set_pin_mode_tone(self, pin_number):
        """
        This is FirmataExpress feature.

        Set a PWM pin to tone mode.

        :param pin_number: arduino pin number

        """
        command = [PrivateConstants.SET_PIN_MODE, pin_number,
                   PrivateConstants.TONE]
        self._send_command(command)

    def _set_pin_mode(self, pin_number, pin_state, callback=None,
                      differential=1):
        """
        A private method to set the various pin modes.

        :param pin_number: arduino pin number

        :param pin_state: INPUT/OUTPUT/ANALOG/PWM/PULLUP
                         For SERVO use: set_pin_mode_servo
                         For DHT   use: set_pin_mode_dht

        :param callback: A reference to a call back function to be
                         called when pin data value changes

        :param differential: This value needs to be met for a callback
                             to be invoked

        """
        if callback:
            if pin_state == PrivateConstants.INPUT:
                self.digital_pins[pin_number].cb = callback
            elif pin_state == PrivateConstants.PULLUP:
                self.digital_pins[pin_number].cb = callback
                self.digital_pins[pin_number].pull_up = True
            elif pin_state == PrivateConstants.ANALOG:
                self.analog_pins[pin_number].cb = callback
                self.analog_pins[pin_number].differential = differential
            else:
                print('{} {}'.format('set_pin_mode: callback ignored for '
                                     'pin state:', pin_state))

        pin_mode = pin_state

        if pin_mode == PrivateConstants.ANALOG:
            pin_number = pin_number + self.first_analog_pin

        command = [PrivateConstants.SET_PIN_MODE, pin_number, pin_mode]
        self._send_command(command)

        if pin_state == PrivateConstants.INPUT or pin_state == PrivateConstants.PULLUP:
            self.enable_digital_reporting(pin_number)
        else:
            pass

    def set_sampling_interval(self, interval):
        """
        This method sends the desired sampling interval to Firmata.

        Note: Standard Firmata  will ignore any interval less than
              10 milliseconds

        :param interval: Integer value for desired sampling interval
                         in milliseconds

        """
        data = [interval & 0x7f, (interval >> 7) & 0x7f]
        self._send_sysex(PrivateConstants.SAMPLING_INTERVAL, data)

    def servo_write(self, pin, position):
        """
        This is an alias for analog_write to set
        the position of a servo that has been
        previously configured using set_pin_mode_servo.

        :param pin: arduino pin number

        :param position: servo position

        """

        self.pwm_write(pin, position)

    def shutdown(self):
        """
        This method attempts an orderly shutdown
        If any exceptions are thrown, they are ignored.

        """

        self.shutdown_flag = True

        self._stop_threads()

        try:
            # stop all reporting - both analog and digital
            for pin in range(len(self.analog_pins)):
                self.disable_analog_reporting(pin)

            for pin in range(len(self.digital_pins)):
                self.disable_digital_reporting(pin)
            self.send_reset()
            if self.ip_address:
                try:
                    self.sock.shutdown(socket.SHUT_RDWR)
                    self.sock.close()
                except Exception:
                    pass
            else:
                self.serial_port.reset_input_buffer()
                self.serial_port.close()

        except (RuntimeError, SerialException, OSError):
            # ignore error on shutdown
            pass

    def sonar_read(self, trigger_pin):
        """
        This is a FirmataExpress feature

        Retrieve Ping (HC-SR04 type) data. The data is presented as a
        dictionary.

        The 'key' is the trigger pin specified in sonar_config()
        and the 'data' is the current measured distance (in centimeters)
        for that pin. If there is no data, the value is set to None.

        :param trigger_pin: key into sonar data map

        :returns: A list = [last value, raw time_stamp]

        """

        sonar_pin_entry = self.active_sonar_map.get(trigger_pin)
        if sonar_pin_entry:
            return [sonar_pin_entry[1], sonar_pin_entry[2]]
        else:
            return [0, 0]

    def stepper_write(self, motor_speed, number_of_steps):
        """
        This is a FirmataExpress feature

        Move a stepper motor for the number of steps at the specified speed.

        :param motor_speed: 21 bits of data to set motor speed

        :param number_of_steps: 14 bits for number of steps & direction
                                positive is forward, negative is reverse

        """
        if number_of_steps > 0:
            direction = 1
        else:
            direction = 0
        abs_number_of_steps = abs(number_of_steps)
        data = [PrivateConstants.STEPPER_STEP, motor_speed & 0x7f,
                (motor_speed >> 7) & 0x7f, (motor_speed >> 14) & 0x7f,
                abs_number_of_steps & 0x7f, (abs_number_of_steps >> 7) & 0x7f,
                direction]
        self._send_sysex(PrivateConstants.STEPPER_DATA, data)

    '''
    Firmata message handlers
    '''

    def _analog_mapping_response(self, data):
        """
        This is a private message handler method.
        It is a message handler for the analog mapping response message.

        :param data: response data

        """
        self.query_reply_data[PrivateConstants.ANALOG_MAPPING_RESPONSE] = data

    def _analog_message(self, data):
        """
        This is a private message handler method.
        It is a message handler for analog messages.

        :param data: message data

        """
        pin = data[0]
        value = (data[PrivateConstants.MSB] << 7) + data[PrivateConstants.LSB]

        # only report when there is a change in value
        differential = abs(value - self.analog_pins[pin].current_value)
        if differential >= self.analog_pins[pin].differential:
            self.analog_pins[pin].current_value = value
            time_stamp = time.time()
            self.analog_pins[pin].event_time = time_stamp

            # append pin number, pin value, and pin type to return value and return as a list
            message = [PrivateConstants.ANALOG, pin, value, time_stamp]

            if self.analog_pins[pin].cb:
                self.analog_pins[pin].cb(message)

    def _capability_response(self, data):
        """
        This is a private message handler method.
        It is a message handler for capability report responses.

        :param data: capability report

        """
        self.query_reply_data[PrivateConstants.CAPABILITY_RESPONSE] = data

    def _dht_read_response(self, data):
        """
        Process the dht response message.

        Values are calculated using:
                humidity = (_bits[0] * 256 + _bits[1]) * 0.1

                temperature = ((_bits[2] & 0x7F) * 256 + _bits[3]) * 0.1

        error codes:
        0 - OK
        1 - DHTLIB_ERROR_TIMEOUT
        2 - Checksum error

        :param: data - array of 9 7bit bytes ending with the error status
        """
        # get the time of the report
        time_stamp = time.time()
        # initiate a list for a potential call back
        reply_data = [PrivateConstants.DHT]

        # get the pin and type of the dht
        pin = data[0]
        reply_data.append(pin)
        dht_type = data[1]
        reply_data.append(dht_type)
        humidity = None
        temperature = None

        self.digital_pins[pin].event_time = time_stamp

        if data[7] == 1:  # data[9] is config flag
            if data[10] != 0:
                self.dht_sensor_error = True
                humidity = temperature = -1
                # return
        else:
            # if data read correctly process and return

            if data[6] == 0:
                # dht 22
                if data[1] == 22:
                    humidity = (data[2] * 256 + data[3]) * 0.1
                    temperature = ((data[4] & 0x7F) * 256 + data[5]) * 0.1
                # dht 11
                elif data[1] == 11:
                    humidity = (data[2]) + (data[3]) * 0.1
                    temperature = (data[4]) + (data[5]) * 0.1
                else:
                    raise RuntimeError(f'Unknown DHT Sensor type reported: {data[2]}')

                humidity = round(humidity, 2)
                temperature = round(temperature, 2)

                # check for negative temperature
                if data[6] & 0x80:
                    temperature = -temperature

            elif data[7] == 1:
                # Checksum Error
                humidity = temperature = -2
                self.dht_sensor_error = True
            elif data[7] == 2:
                # Timeout Error
                humidity = temperature = -3
                self.dht_sensor_error = True
        # since we initialize
        if humidity is None:
            return
        reply_data.append(humidity)
        reply_data.append(temperature)
        reply_data.append(time_stamp)

        # retrieve the last reported values
        last_value = self.digital_pins[pin].current_value

        self.digital_pins[pin].current_value = [humidity, temperature]
        if self.digital_pins[pin].cb:
            # only report changes
            # has the humidity changed?
            if last_value[0] != humidity:

                differential = abs(humidity - last_value[0])
                if differential >= self.digital_pins[pin].differential:
                    self.digital_pins[pin].cb(reply_data)
                return
            if last_value[1] != temperature:
                differential = abs(temperature - last_value[1])
                if differential >= self.digital_pins[pin].differential:
                    self.digital_pins[pin].cb(reply_data)
                return

    def _digital_message(self, data):
        """
        This is a private message handler method.
        It is a message handler for Digital Messages.

        :param data: digital message

        """
        port = data[0]
        # noinspection PyPep8
        port_data = (data[PrivateConstants.MSB] << 7) + data[PrivateConstants.LSB]
        pin = port * 8
        for pin in range(pin, min(pin + 8, len(self.digital_pins))):
            # get pin value
            value = port_data & 0x01

            # retrieve previous value
            last_value = self.digital_pins[pin].current_value

            # set the current value in the pin structure
            self.digital_pins[pin].current_value = value
            time_stamp = time.time()
            self.digital_pins[pin].event_time = time_stamp

            # append pin number, pin value, and pin type to return value and return as a list
            if self.digital_pins[pin].pull_up:
                message = [PrivateConstants.PULLUP, pin, value, time_stamp]
            else:
                message = [PrivateConstants.INPUT, pin, value, time_stamp]

            if last_value != value:
                if self.digital_pins[pin].cb:
                    self.digital_pins[pin].cb(message)

            port_data >>= 1

    # noinspection PyDictCreation

    def _i2c_reply(self, data):
        """
        This is a private message handler method.
        It handles replies to i2c_read requests. It stores the data
        for each i2c device address in a dictionary called i2c_map.
        The data may be retrieved via a polling call to i2c_get_read_data().
        It a callback was specified in pymata.i2c_read, the raw data is sent
        through the callback

        :param data: raw data returned from i2c device

        """
        # initialize the reply data with I2C pin mode
        reply_data = [PrivateConstants.I2C]
        # reassemble the data from the firmata 2 byte format
        address = (data[0] & 0x7f) + (data[1] << 7)

        # if we have an entry in the i2c_map, proceed
        if address in self.i2c_map:
            with self.the_i2c_map_lock:
                # get 2 bytes, combine them and append to reply data list
                for i in range(0, len(data), 2):
                    combined_data = (data[i] & 0x7f) + (data[i + 1] << 7)
                    reply_data.append(combined_data)

                current_time = time.time()
                reply_data.append(current_time)

                # place the data in the i2c map without storing the address byte or
                #  register byte (returned data only)
                map_entry = self.i2c_map.get(address)
                map_entry['value'] = reply_data[3:]
                map_entry['time_stamp'] = current_time
                self.i2c_map[address] = map_entry
                cb = map_entry.get('callback')
                if cb:
                    # send everything, including address and register bytes back
                    # to caller
                    # reply data will contain:
                    # [pin_type = 6, i2c_device address,
                    #                       raw data returned from i2c device, time-stamp]
                    cb(reply_data)

    def _pin_state_response(self, data):
        """
        This is a private message handler method.
        It handles pin state query response messages.

        :param data: Pin state message

        """
        self.query_reply_data[PrivateConstants.PIN_STATE_RESPONSE] = data

    def _report_firmware(self, sysex_data):
        """
        This is a private message handler method.

        This method handles the sysex 'report firmware' command sent by
        Firmata (0x79).

        It assembles the firmware version by concatenating the major and
        minor version number components and the firmware identifier into
        a string.

        e.g. "2.3 StandardFirmata.ino"

        :param sysex_data: Sysex data sent from Firmata

        """
        # first byte after command is major number
        major = sysex_data[0]
        version_string = str(major)

        # next byte is minor number
        # minor = sysex_data[2]
        minor = sysex_data[1]

        # append a dot to major number
        version_string += '.'

        # append minor number
        version_string += str(minor)
        # add a space after the major and minor numbers
        version_string += ' '

        # slice the identifier - from the first byte after the minor
        #  number up until, but not including the END_SYSEX byte

        # name = sysex_data[3:-1]
        name = sysex_data[2:]

        firmware_name_iterator = iter(name)

        # convert each element from two 7-bit bytes into characters, then add each
        # character to the version string
        for e in firmware_name_iterator:
            version_string += chr(e + (next(firmware_name_iterator) << 7))

        # store the value
        self.query_reply_data[PrivateConstants.REPORT_FIRMWARE] = version_string

    def _report_version(self, data):
        """
        This is a private message handler method.

        This method reads the following 2 bytes after the report version
        command (0xF9 - non sysex).

        The first byte is the major number and the second byte is the
        minor number.

        """
        version_string = str(data[0]) + '.' + str(data[1])
        self.query_reply_data[PrivateConstants.REPORT_VERSION] = version_string

    def _send_command(self, command):
        """
        This is a private utility method.
        The method sends a non-sysex command to Firmata.

        :param command:  command data

        :returns: number of bytes sent
        """
        # send_message = ""
        send_message = bytes(command)
        if not self.ip_address:
            try:
                result = self.serial_port.write(send_message)
            except SerialException:
                if self.shutdown_on_exception:
                    self.shutdown()
                raise RuntimeError('write fail in _send_command')
            return result
        else:
            self.sock.sendall(send_message)

    def _send_keep_alive(self):
        """
        This is a the thread to continuously send keep alive messages
        """
        while True:
            if self.period:
                self._send_sysex(PrivateConstants.KEEP_ALIVE,
                                 self.keep_alive_interval)
                time.sleep(self.period - self.margin)
            else:
                break

    def _sonar_data(self, data):
        """
        This method handles the incoming sonar data message and stores
        the data in the response table.

        :param data: Message data from Firmata

        """

        pin_number = data[0]
        val = int((data[PrivateConstants.MSB] << 7) +
                  data[PrivateConstants.LSB])
        # initialize reply_data with SONAR pin type
        reply_data = [PrivateConstants.SONAR]

        with self.the_sonar_map_lock:
            sonar_pin_entry = self.active_sonar_map[pin_number]
            if sonar_pin_entry[0] is not None:
                # check if value changed since last reading
                if sonar_pin_entry[1] != val:
                    sonar_pin_entry[1] = val
                    time_stamp = time.time()
                    sonar_pin_entry[2] = time_stamp
                    self.active_sonar_map[pin_number] = sonar_pin_entry
                    # Do a callback if one is specified in the table
                    if sonar_pin_entry[0]:
                        reply_data.append(pin_number)
                        reply_data.append(val)
                        reply_data.append(time_stamp)
                        if sonar_pin_entry[1]:
                            sonar_pin_entry[0](reply_data)

                # update the data in the table with latest value
                else:
                    sonar_pin_entry[1] = val
                    self.active_sonar_map[pin_number] = sonar_pin_entry
            time.sleep(self.sleep_tune)

    def _send_sysex(self, sysex_command, sysex_data=None):
        """
        This is a private utility method.
        This method sends a sysex command to Firmata.

        :param sysex_command: sysex command

        :param sysex_data: data for command

        """
        if not sysex_data:
            sysex_data = []

        the_command = [PrivateConstants.START_SYSEX, sysex_command]
        if sysex_data:
            for d in sysex_data:
                the_command.append(d)
        the_command.append(PrivateConstants.END_SYSEX)
        with self.the_send_sysex_lock:
            self._send_command(the_command)

    # noinspection PyMethodMayBeStatic
    def _string_data(self, data):
        """
        This is a private message handler method.
        It is the message handler for String data messages that will be
        printed to the console.

        :param data:  message

        """
        reply = ''
        for x in data:
            reply_data = x
            if reply_data:
                reply += chr(reply_data)
        print(reply)

    def _run_threads(self):
        self.run_event.set()

    def _is_running(self):
        return self.run_event.is_set()

    def _stop_threads(self):
        self.run_event.clear()

    def _reporter(self):
        """
        This is the reporter thread. It continuously pulls data from
        the deque. When a full message is detected, that message is
        processed.
        """
        self.run_event.wait()

        # sysex commands are assembled into this list for processing
        # next_command_byte = None
        while self._is_running() and not self.shutdown_flag:
            if len(self.the_deque):

                # get next byte from the deque and process it
                data = self.the_deque.popleft()

                # this list will be populated with the received data for the command
                response_data = []

                # process sysex commands
                if data == PrivateConstants.START_SYSEX:
                    # next char is the actual sysex command
                    # wait until we can get data from the deque
                    while len(self.the_deque) == 0:
                        pass
                    sysex_command = self.the_deque.popleft()
                    # retrieve the associated command_dispatch entry for this command
                    dispatch_entry = self.report_dispatch.get(sysex_command)

                    # get a "pointer" to the method that will process this command
                    method = dispatch_entry[0]

                    # now get the rest of the data excluding the END_SYSEX byte
                    end_of_sysex = False
                    while not end_of_sysex:
                        # wait for more data to arrive
                        while len(self.the_deque) == 0:
                            pass
                        data = self.the_deque.popleft()
                        if data != PrivateConstants.END_SYSEX:
                            response_data.append(data)
                        else:
                            end_of_sysex = True

                            # invoke the method to process the command
                            method(response_data)
                            # go to the beginning of the loop to process the next command
                    continue

                # is this a command byte in the range of 0x80-0xff - these are the non-sysex messages

                elif 0x80 <= data <= 0xff:
                    # look up the method for the command in the command dispatch table
                    # for the digital reporting the command value is modified with port number
                    # the handler needs the port to properly process, so decode that from the command and
                    # place in response_data
                    if 0x90 <= data <= 0x9f:
                        port = data & 0xf
                        response_data.append(port)
                        data = 0x90
                    # the pin number for analog data is embedded in the command so, decode it
                    elif 0xe0 <= data <= 0xef:
                        pin = data & 0xf
                        response_data.append(pin)
                        data = 0xe0
                    else:
                        pass

                    dispatch_entry = self.report_dispatch.get(data)

                    # this calls the method retrieved from the dispatch table
                    method = dispatch_entry[0]

                    # get the number of parameters that this command provides
                    num_args = dispatch_entry[1]

                    # look at the number of args that the selected method requires
                    # now get that number of bytes to pass to the called method
                    for i in range(num_args):
                        while len(self.the_deque) == 0:
                            pass
                        data = self.the_deque.popleft()
                        response_data.append(data)
                        # go execute the command with the argument list
                    method(response_data)

                    # go to the beginning of the loop to process the next command
                    continue
            else:
                time.sleep(self.sleep_tune)

    def _serial_receiver(self):
        """
        Thread to continuously check for incoming data.
        When a byte comes in, place it onto the deque.
        """
        self.run_event.wait()

        while self._is_running() and not self.shutdown_flag:
            # we can get an OSError: [Errno9] Bad file descriptor when shutting down
            # just ignore it
            try:
                if self.serial_port.inWaiting():
                    c = self.serial_port.read()
                    self.the_deque.append(ord(c))
                else:
                    time.sleep(self.sleep_tune)
                    # continue
            except OSError:
                pass

    def _tcp_receiver(self):
        """
        Thread to continuously check for incoming data.
        When a byte comes in, place it onto the deque.
        """
        self.run_event.wait()
        while self._is_running() and not self.shutdown_flag:
            try:
                payload = self.sock.recv(1)
                self.the_deque.append(ord(payload))
            except Exception:
                pass
