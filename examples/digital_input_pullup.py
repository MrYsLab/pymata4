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


import sys
import time

from pymata4 import pymata4

"""
Setup a digital pin for input pullup and monitor its changes.
"""

# some globals
DIGITAL_PIN = 12  # arduino pin number
KILL_TIME = 5  # sleep time to keep forever loop open

# Callback data indices
# Callback data indices
CB_PIN_MODE = 0
CB_PIN = 1
CB_VALUE = 2
CB_TIME = 3


# Setup a pin for digital pin input and monitor its changes

def the_callback(data):
    """
    A callback function to report data changes.
    This will print the pin number, its reported value and
    the date and time when the change occurred

    :param data: [pin, current reported value, pin_mode, timestamp]
    """
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[CB_TIME]))
    print(f'Pin: {data[CB_PIN]} Value: {data[CB_VALUE]} Time Stamp: {date}')


def digital_in_pullup(my_board, pin):
    """
     This function establishes the pin as a
     digital input. Any changes on this pin will
     be reported through the call back function.

     :param my_board: a pymata4 instance
     :param pin: Arduino pin number
     """

    # start monitoring the pin by setting its mode
    my_board.set_pin_mode_digital_input_pullup(pin, callback=the_callback)

    # get pin changes forever
    while True:
        try:
            time.sleep(KILL_TIME)
        except KeyboardInterrupt:
            board.shutdown()
            sys.exit(0)


board = pymata4.Pymata4()
try:
    digital_in_pullup(board, DIGITAL_PIN)
    board.shutdown()
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
