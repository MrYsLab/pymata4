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
Setup a pin for dht mode
One pin is set for a dht22 and another for dht11
Both polling and callback are being used in this example.
"""

#
POLL_TIME = 5  # number of seconds between polls

# Callback data indices
CB_PIN_MODE = 0
CB_PIN = 1
CB_VALUE = 2
CB_TIME = 3


def the_callback(data):
    """
    A callback function to report data changes.
    This will print the pin number, its reported value and
    the date and time when the change occurred

    :param data: [pin, current reported value, pin_mode, timestamp]
    """

    tlist = time.localtime(data[5])
    ftime = f'{tlist.tm_year}-{tlist.tm_mon:02}-{tlist.tm_mday:02} ' \
            f'{tlist.tm_hour:02}:{tlist.tm_min:0}:{tlist.tm_sec:02}'

    print(f'Pin: {data[1]} DHT Type: {data[2]} Humidity:{data[3]}, '
          f'Temperature: {data[4]} Timestamp: {ftime}')


def dht(my_board, callback=None):
    """
     This function establishes the pin as a
     digital input. Any changes on this pin will
     be reported through the call back function.

     :param my_board: a pymata4 instance
     :param callback: callback funtion
     """

    # set the pin mode - for pin 6 differential is set explicitly
    my_board.set_pin_mode_dht(6, sensor_type=22, differential=.01, callback=callback)
    my_board.set_pin_mode_dht(7, sensor_type=11, callback=callback)

    # a flag to change the differential value after the first 5 seconds
    changed = False
    while True:
        try:
            time.sleep(POLL_TIME)

            # poll the first DHT
            value = board.dht_read(6)

            # format the time string and then print the data
            tlist = time.localtime(value[2])
            ftime = f'{tlist.tm_year}-{tlist.tm_mon:02}-{tlist.tm_mday:02} ' \
                    f'{tlist.tm_hour:02}:{tlist.tm_min:0}:{tlist.tm_sec:02}'
            print(f'poll pin 6: humidity={value[0]} temp={value[1]} '
                  f'time of last report: {ftime}')

            # poll the second DHT and print the values
            value = board.dht_read(7)
            tlist = time.localtime(value[2])
            ftime = f'{tlist.tm_year}-{tlist.tm_mon:02}-{tlist.tm_mday:02} ' \
                    f'{tlist.tm_hour:02}:{tlist.tm_min:0}:{tlist.tm_sec:02}'
            print(f'poll pin 7: humidity={value[0]} temp={value[1]} '
                  f'time of last report: {ftime}')
            if not changed:
                # explicitly change the differential values
                my_board.set_pin_mode_dht(6, sensor_type=22, differential=20.0, callback=callback)
                my_board.set_pin_mode_dht(7, sensor_type=22, differential=2.0, callback=callback)
                changed = True
        except KeyboardInterrupt:
            board.shutdown()
            sys.exit(0)


board = pymata4.Pymata4()

try:
    dht(board, the_callback)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
