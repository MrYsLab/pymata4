# pymata4

### A high performance, Python client for the Arduino Firmata Protocol.
Pymata4 is a Firmata client that, like its asyncio sibling,
 [pymata-express,](https://mryslab.github.io/pymata-express/)
 allows you to control an Arduino using the high-performance FirmataExpress sketch.
  It uses a conventional Python API for those that do not need or wish to use the asyncio programming paradigm of pymata-express.

### A [User's Guide is available,](https://mryslab.github.io/pymata4/) containing an annotated API as well as links to working examples.

### It supports both an enhanced version of StandardaFirmata 2.5.8, called FirmataExpress, as well as StandardFirmata. 
* **[FirmataExpress](https://github.com/MrYsLab/FirmataExpress) adds support for:**
     * **HC-SR04 Ultrasonic Distance Sensors using a single pin.**
     * **Stepper Motors.**
     * **Piezo Tone Generation.**
     * **Baud rate of 115200**

<h2><u>Major features</u></h2>

* **Fully documented <a href="https://htmlpreview.github.com/?https://github.com/MrYsLab/pymata4/blob/master/html/pymata4/index.html" target="_blank">intuitive API</a>**


* **Python 3.7+ compatible.**

* **Set the pin mode and go!**

* **Data change events may be associated with a callback function, or each pin can be polled for its last event change.**

    * **Each data change event is time-stamped and logged.**

* **[User's Guide](https://mryslab.github.io/pymata4/), Including Examples.**

* **Implements 100% of the StandardFirmata Protocol (StandardFirmata 2.5.8).**

* **Advanced auto-detection of Arduino devices (when using FirmataExpress).**

Here is an example that monitors data changes on a digital input pin. It demonstrates both callback and 
polling techniques

```python
import time
import sys
from pymata4 import pymata4

"""
Setup a pin for digital input and monitor its changes
Both polling and callback are being used in this example.
"""

# Setup a pin for analog input and monitor its changes
DIGITAL_PIN = 12  # arduino pin number
POLL_TIME = 5  # number of seconds between polls

# Callback data indices
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
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[CB_TIME]))
    print(f'Pin: {data[CB_PIN]} Value: {data[CB_VALUE]} Time Stamp: {date}')


def digital_in(my_board, pin):
    """
     This function establishes the pin as a
     digital input. Any changes on this pin will
     be reported through the call back function.

     :param my_board: a pymata_express instance
     :param pin: Arduino pin number
     """

    # set the pin mode
    my_board.set_pin_mode_digital_input(pin, callback=the_callback)

    while True:
        try:
            # Do a read of the last value reported every 5 seconds and print it
            # digital_read returns A tuple of last value change and the time that it occurred
            value, time_stamp = my_board.digital_read(pin)
            date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_stamp))
            # value
            print(f'Polling - last value: {value} received on {date} ')
            time.sleep(POLL_TIME)
        except KeyboardInterrupt:
            board.shutdown()
            sys.exit(0)

board = pymata4.Pymata4()

try:
    digital_in(board, DIGITAL_PIN)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)

```
     
And here is the console output:
```bash
pymata4:  Version 1.00

Copyright (c) 2020 Alan Yorinks All Rights Reserved.

Opening all potential serial ports...
	/dev/ttyACM0

Waiting 4 seconds(arduino_wait) for Arduino devices to reset...

Searching for an Arduino configured with an arduino_instance = 1
Arduino compatible device found and connected to /dev/ttyACM0

Retrieving Arduino Firmware ID...
Arduino Firmware ID: 2.5 FirmataExpress.ino

Retrieving analog map...
Auto-discovery complete. Found 20 Digital Pins and 6 Analog Pins


Polling - last change: 0 change received on 1969-12-31 19:00:00 
Pin: 12 Value: 0 Time Stamp: 2020-03-07 08:52:10
Pin: 12 Value: 1 Time Stamp: 2020-03-07 08:52:12
Polling - last value: 1 received on 2020-03-07 08:52:12 
```


This project was developed with [Pycharm](https://www.jetbrains.com/pycharm/?from=pymata4) ![logo](https://github.com/MrYsLab/python_banyan/blob/master/images/icon_PyCharm.png)
