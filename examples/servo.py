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
This example will set a servo to 0, 90 and 180 degree
positions.
"""


def servo(my_board, pin):
    """
    Set a pin to servo mode and then adjust
    its position.

    :param my_board: pymata_express instance
    :param pin: pin to be controlled
    """

    # set the pin mode
    my_board.set_pin_mode_servo(pin)

    # set the servo to 0 degrees
    my_board.servo_write(pin, 0)
    time.sleep(1)
    # set the servo to 90 degrees
    my_board.servo_write(pin, 90)
    time.sleep(1)
    # set the servo to 180 degrees
    my_board.servo_write(pin, 180)


board = pymata4.Pymata4()

try:
    servo(board, 5)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
