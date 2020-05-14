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
This program tests an ESP-8266 using StandardFirmataWiFi.
It will toggle the on-board LED 4 times.

Change the IP address and IP port to match that in the
StandardFirmataWiFi config file.
"""

# some globals
DIGITAL_PIN = 16  # arduino pin number
IP_ADDRESS = "192.168.2.189"
IP_PORT = 3030


def blink(my_board, pin):
    """
    This function will to toggle a digital pin.

    :param my_board: an PymataExpress instance
    :param pin: pin to be controlled
    """

    # set the pin mode
    my_board.set_pin_mode_digital_output(pin)
    my_board.digital_write(pin, 1)

    # toggle the pin 4 times and exit
    for x in range(4):
        print('ON')
        my_board.digital_write(pin, 1)
        time.sleep(1)
        print('OFF')
        my_board.digital_write(pin, 0)
        time.sleep(1)

    my_board.shutdown()


board = pymata4.Pymata4(ip_address=IP_ADDRESS, ip_port=IP_PORT)
try:
    blink(board, DIGITAL_PIN)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
