"""
 Copyright (c) 2020 Alan Yorinks All rights reserved.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import argparse
import sys
import time
from pymata4 import pymata4

"""
This file demonstrates analog input using both callbacks and
polling. Time stamps are provided in both "cooked" and raw form.

This is an object oriented example of the the analog_input_with_time_stamps
example using argparse to allow command line entry of the pin, poll-time and 
differential values.
"""


class MonitorAnalogPin:

    def __init__(self, analog_pin=2, poll_time=5, differential=5):
        """

        :param analog_pin: arduino analog input pin number

        :param poll_time: polling interval in seconds

        :param differential: difference between current value and
                             previous value to consider the change
                             in value a change event
        """
        self.analog_pin = analog_pin
        self.poll_time = poll_time
        self.differential = differential

        # Callback data indices
        self.CB_PIN_MODE = 0  # pin mode (see pin modes in private_constants.py)
        self.CB_PIN = 1  # pin number
        self.CB_VALUE = 2  # reported value
        self.CB_TIME = 3  # raw time stamp

        # instantiate pymata4
        self.board = pymata4.Pymata4()

        # set the pin mode for analog input
        self.board.set_pin_mode_analog_input(self.analog_pin, self.the_callback, self.differential)

        # start polling
        self.keep_polling()

    def keep_polling(self):
        """
        A forever loop.
        Poll the selected pin at the specified poll interval and print out
        the last value received.
        """
        try:
            while True:
                time.sleep(self.poll_time)
                # retrieve both the value and time stamp with each poll
                value, time_stamp = self.board.analog_read(self.analog_pin)
                # format the time stamp
                formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_stamp))
                print(
                    f'Reading latest analog input data for pin {self.analog_pin} = {value} '
                    f'change received on  {formatted_time} '
                    f'(raw_time: {time_stamp})')
        except KeyboardInterrupt:
            self.board.shutdown()
            sys.exit(0)

    def the_callback(self, data):
        """
        A callback function to report data changes.

        :param data: [pin_mode, pin, current_reported_value,  timestamp]

        """
        print(data[self.CB_TIME])
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[self.CB_TIME]))
        print(f'Analog Call Input Callback: pin={data[self.CB_PIN]}, '
              f'Value={data[self.CB_VALUE]} Time={formatted_time} '
              f'(Raw Time={data[self.CB_TIME]})')


def monitor_analog_pin():
    # noinspection PyShadowingNames

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="differential", default=5,
                        help="Set reporting differential - default = 5")
    parser.add_argument("-p", dest="analog_pin", default=2,
                        help="Arduino analog pin number - default = 2")
    parser.add_argument("-t", dest="poll_time", default=5,
                        help="Poll Time In Seconds - default = 5")

    args = parser.parse_args()

    MonitorAnalogPin(analog_pin=int(args.analog_pin),
                     differential=int(args.differential),
                     poll_time=int(args.poll_time))


if __name__ == '__main__':
    monitor_analog_pin()
