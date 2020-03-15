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


# This example tests multi-threading by
# enabling many things at once

def the_callback(data):
    print(data)


def stress_test(my_board, loop_count):
    print(f'Iterating {loop_count} times.')

    my_board.set_pin_mode_digital_input(12, callback=the_callback)
    my_board.set_pin_mode_digital_input(13, callback=the_callback)
    my_board.set_pin_mode_analog_input(2, callback=the_callback)
    my_board.set_pin_mode_pwm_output(9)
    my_board.set_pin_mode_digital_output(6)

    start_time = time.time()

    for x in range(loop_count):
        my_board.digital_pin_write(6, 1)
        my_board.pwm_write(9, 255)
        my_board.analog_read(2)
        time.sleep(.00001)
        my_board.digital_pin_write(6, 0)
        my_board.pwm_write(9, 0)
        my_board.digital_read(13)
        time.sleep(.00001)

    print(f'Execution time: {time.time() - start_time} seconds for {loop_count} iterations.')


board = pymata4.Pymata4()
try:
    stress_test(board, 10000)
    board.shutdown()
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
