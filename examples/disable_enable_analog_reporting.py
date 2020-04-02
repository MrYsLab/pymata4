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

import time
import sys
from pymata4 import pymata4

"""
Test disable and enable analog reporting
"""

# Setup a pin for analog input and monitor its changes
ANALOG_PIN = 2  # arduino pin number


def the_callback(data):
    """
    A callback function to report raw data changes.

    :param data: [pin, current reported value, pin_mode, timestamp]
    """

    print(data)


def analog_reporting(my_board, pin):
    """
     This function will enable the analog input pin.
     It then allows you to manipulate the pin for 5
     seconds before disabling reporting.

     Next it waits another 5 seconds with reporting disabled
     allowing you to manipulate the pin to verify that
     callbacks are not generated

     :param my_board: a pymata4 instance
     :param pin: Arduino pin number
     """

    # set the pin mode
    try:
        my_board.set_pin_mode_analog_input(pin, callback=the_callback)

        # start a 5 second period for you to manipulate the 5
        print('You have 5 seconds to manipulate the pin input.')

        time.sleep(5)
        value, time_stamp = my_board.analog_read(pin)
        print(f'Print polling the pin: value = {value} ')

        my_board.disable_analog_reporting(pin)

        print('Reporting is disabled. You have another 5 seconds '
              'to manipulate the pin to see that reporting has ceased')
        value, time_stamp = my_board.analog_read(pin)
        time.sleep(5)

        print(f'Print polling the pin: value = {value} ')

        my_board.enable_analog_reporting(pin, callback=the_callback)

        print('Reporting is now re-enabled. You have 5 seconds to '
              'manipulate the pin until the program exits')

        time.sleep(5)
        value, time_stamp = my_board.analog_read(pin)
        print(f'Print polling the pin: value = {value} ')
        my_board.shutdown()
        sys.exit(0)

    except KeyboardInterrupt:
        my_board.shutdown()
        sys.exit(0)


board = pymata4.Pymata4()

try:
    analog_reporting(board, ANALOG_PIN)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
