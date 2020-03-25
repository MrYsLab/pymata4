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

import time
import sys
from pymata4 import pymata4

"""
Demonstrate the keep-alive functionality
of FirmataExpress.
NOTE: This only works with ATmega328P processors, such
as used by the Arduino Uno.
"""


def keep_alive_test(pin_number):
    """
    This program will set a digital output pin to high.
    It is assumed that an LED is connected to this pin.
    After 2 seconds the program exits, and in approximately
    one second the LED should extinguish.

    If keep_alive is working, the LED should extinguish.

    :param pin_number: A pin with an LED connected to it
    """

    board = pymata4.Pymata4()

    # set the as a digital output
    board.set_pin_mode_digital_output(pin_number)

    # set the pin high
    board.digital_write(pin_number, 1)

    # turn on keep_alives
    board.keep_alive()

    print('Sleeping for 2 seconds...')
    time.sleep(2)
    print('Exiting. In about 1 second, the LED should extinguish.')
    sys.exit(0)


keep_alive_test(6)
