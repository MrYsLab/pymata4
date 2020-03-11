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
This example demonstrates running a stepper motor
"""
NUM_STEPS = 512
ARDUINO_PINS = [8, 9, 10, 11]


def stepper(my_board, steps_per_rev, pins):
    """
    Set the motor control control pins to stepper mode.
    Rotate the motor.

    :param my_board: pymata_express instance
    :param steps_per_rev: Number of steps per motor revolution
    :param pins: A list of the motor control pins
    """

    my_board.set_pin_mode_stepper(steps_per_rev, pins)
    time.sleep(1)
    my_board.stepper_write(20, 500)


board = pymata4.Pymata4()
try:
    stepper(board, NUM_STEPS, ARDUINO_PINS)
    board.shutdown()
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
