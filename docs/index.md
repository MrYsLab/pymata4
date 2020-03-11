

<div style="text-align:center;color:#990033; font-family:times, serif; font-size:6.5em"><i>pymata4</i></div>
<br>
<br>

[Pymata4](https://github.com/MrYsLab/pymata4) is a Python Arduino Firmata
client that, like its asyncio sibling [pymata-express](https://mryslab.github.io/pymata4/)
allows you to control an Arduino using the high-performance FirmataExpress sketch. But unlike
pymata-express, it uses a conventional 
[Python API](https://htmlpreview.github.com/?https://github.com/MrYsLab/pymata4/blob/master/html/pymata4/index.html)
for those that do not need or wish to use an asycnio
programming paradigm.

When used with the [FirmataExpress](https://github.com/MrYsLab/FirmataExpress) Arduino sketch,
the serial data rate is 115200 baud, twice the speed of StandardFirmata. FirmataExpress,
is based on [StandardFirmata 2.5.8 protocol,](https://github.com/firmata/protocol/blob/master/protocol.md),
 and adds support for
stepper motors, tone generation, HC-SRO4 distance sensors, and the auto-detection of Arduino boards.

If you prefer to work with StandardFirmata Pymata Express is compatible with it as well.

The pymata4 API is intuitive and easy to use. Essentially, just set a pin mode, specify a callback function, 
and wait for pin state changes.

Here is an object-oriented example that monitors digital pin 12 for state changes:

```python
from pymata4 import pymata4
import time

class DigitalInput:
    """
    Set a pin for digital input and received all data changes
    in the callback method
    """
    def __init__(self, pin):
        """
        Set a pin as a digital input
        :param pin: digital pin number
        """

        # Indices into the callback report data
        self.CB_PIN = 0
        self.CB_VALUE = 1
        self.CB_PIN_MODE = 2
        self.CB_TIME = 3

        # Instantiate this class with the pymata4 API
        self.device = pymata4.Pymata4()

        # Set the pin mode and specify the callback method.
        self.device.set_pin_mode_digital_input(pin, callback=self.the_callback)

        # Keep the program running and wait for callback events.
        while True:
            try:
                time.sleep(1)
            # If user hits Control-C, exit cleanly.
            except KeyboardInterrupt:
                self.device.shutdown()

    def the_callback(self, data):
        """
        A callback function to report data changes.
        This will print the pin number, its reported value
        the pin type (digital, analog, etc.) and
        the date and time when the change occurred

        :param data: [pin, current reported value, pin_mode, timestamp]
        """
        # Convert the date stamp to readable format
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[self.CB_TIME]))

        # Print the pin, current value and time and date of the pin change event.
        print(f'Pin: {data[self.CB_PIN]} Value: {data[self.CB_VALUE]} Time Stamp: {date}')

if __name__ == '__main__':
    # Monitor Pin 12 For Digital Input changes
    DigitalInput(12)
```

Sample console output as input change events occur:
```python
Pin: 12 Value: 0 Time Stamp: 2020-03-10 13:26:22
Pin: 12 Value: 1 Time Stamp: 2020-03-10 13:26:27
```

A full set of [working examples
 is available on GitHub.](https://github.com/MrYsLab/pymata4/tree/master/examples)
  These examples demonstate
pymata4's entire feature set.

Installation and system requirements are provided in the following sections
of this document:

* [Verifying The Python 3 Version.](/python_3_verify/#how-to-verify-the-python-3-version-installed) 
* [Python 3 Installation Instructions.](/python_install/#installing-python-37-or-greater)
* [Installing _pymata4_.](/install_pymata4/#before-you-install)
* [Installing FirmataExpress On Your Arduino.](/firmata_express/#installation-instruction)


Last updated 12 March 2020 For Release v1.00

Copyright (C) 2020 Alan Yorinks. All Rights Reserved.
