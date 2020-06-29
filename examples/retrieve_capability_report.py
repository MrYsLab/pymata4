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

"""
This is a demo of retrieving a Firmata capability report and
printing a formatted version of the report to the console
"""


def format_capability_report(data):
    """
    This method prints a formatted capability report to the console.

    :param data: Capability report

    :returns: None
    """

    pin_modes = {0: 'Digital_Input', 1: 'Digital_Output',
                 2: 'Analog_Input', 3: 'PWM', 4: 'Servo',
                 6: 'I2C', 8: 'Stepper',
                 11: 'Digital_Input_Pullup', 12: 'HC-SR04_Sonar', 13: 'Tone',
                 15: 'DHT'}
    x = 0
    pin = 0

    print('\nCapability Report')
    print('-----------------\n')
    while x < len(data):
        # get index of next end marker
        print('{} {}{}'.format('Pin', str(pin), ':'))
        while data[x] != 127:
            mode_str = ""
            pin_mode = pin_modes.get(data[x])
            mode_str += str(pin_mode)
            x += 1
            bits = data[x]
            print('{:>5}{}{} {}'.format('  ', mode_str, ':', bits))
            x += 1
        x += 1
        pin += 1


def retrieve_capability_report(my_board):
    """
    Retrieve the report.

    :param my_board: a pymata-express instance
    """
    # get the report
    report = my_board.get_capability_report()

    # print a human readable version
    format_capability_report(report)


# instantiate pymata4
board = pymata4.Pymata4()

try:
    # run the program
    retrieve_capability_report(board)

    # orderly shutdown
    board.shutdown()
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
