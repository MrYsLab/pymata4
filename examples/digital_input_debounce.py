"""
 Copyright (c) 2018-2019 Alan Yorinks All rights reserved.

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

import sys
import time
from pymata4 import pymata4

"""
Setup a pin for digital input and monitor its changes
Both polling and callback are being used in this example.
This demonstrates one possible way to debounce a switch.
"""

# A global to hold the time of the last change detected.
# Used to debounce a switch
previous_change_time = 0

# differential in time to suppress switch bounces
# adjust this to your device "bounciness"
debounce_time = 600

# Setup a pin for analog input and monitor its changes
DIGITAL_PIN = 12  # arduino pin number
POLL_TIME = 5  # number of seconds between polls

# Callback data indices
# Callback data indices
CB_PIN_MODE = 0
CB_PIN = 1
CB_VALUE = 2
CB_TIME = 3


def the_callback(data):
    """
    A callback function to report data changes.
    This will print the pin number, its reported value and
    the date and time when the change occurred

    :param data: [pin, current reported value, pin_mode, timestamp]
    """

    global debounce_time, previous_change_time
    # see if we waited long enough for debounce
    # get the reported change time
    ts_milliseconds = int(round(data[CB_TIME] * 1000))

    if ts_milliseconds - previous_change_time > debounce_time:
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[CB_TIME]))
        print(f'Pin: {data[CB_PIN]} Value: {data[CB_VALUE]} Time Stamp: {date}')
        previous_change_time = ts_milliseconds


def digital_in(my_board, pin):
    """
     This function establishes the pin as a
     digital input. Any changes on this pin will
     be reported through the call back function.

     :param my_board: a pymata_express instance
     :param pin: Arduino pin number
     """

    # set the pin mode
    my_board.set_pin_mode_digital_input(pin, callback=the_callback)

    while True:
        # Do a read of the last value reported every 5 seconds and print it
        # digital_read returns A tuple of last value change and the time that it occurred
        value, time_stamp = my_board.digital_read(pin)
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_stamp))
        print(f'Polling - last change: {value} change received on {date} ')
        time.sleep(POLL_TIME)


board = pymata4.Pymata4()

try:
    digital_in(board, DIGITAL_PIN)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
