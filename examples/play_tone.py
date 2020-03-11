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

# This is a demonstration of the tone methods



# instantiate pymata express
board = pymata4.Pymata4()
TONE_PIN=3
try:
    # set a pin's mode for tone operations
    board.set_pin_mode_tone(TONE_PIN)

    # specify pin, frequency and duration and play tone
    board.play_tone(TONE_PIN, 1000, 500)
    time.sleep(2)

    # specify pin and frequency and play continuously
    board.play_tone_continuously(TONE_PIN, 2000)
    time.sleep(2)

    # specify pin to turn pin off
    board.play_tone_off(TONE_PIN)

    # clean up
    board.shutdown()
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
