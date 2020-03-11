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

from pymata4 import pymata4


# This example manipulates a PWM pin and retrieves its pin
# state after each manipulation


def retrieve_pin_state(my_board):
    """
    Establish a pin as a PWM pin. Set its value
    to 127 and get the pin state. Then set the pin's
    value to zero and get the pin state again.

    :param my_board: pymata_aio instance
    :return: No values returned by results are printed to console
    """
    my_board.set_pin_mode_pwm_output(9)
    my_board.pwm_write(9, 127)
    pin_state = my_board.get_pin_state(9)
    print(f'You should see [9, 3, 127] and have received: {pin_state}')
    my_board.pwm_write(9, 0)
    pin_state = my_board.get_pin_state(9)
    print(f'You should see [9, 3, 0]   and have received: {pin_state}')


board = pymata4.Pymata4()
try:
    retrieve_pin_state(board)
    board.shutdown()
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
