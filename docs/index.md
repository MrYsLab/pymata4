

<div style="text-align:center;color:#990033; font-family:times, serif; font-size:3.5em"><i>pymata4</i></div>
<div style="text-align:center;color:#990033; font-family:times, serif; font-size:2em"><i>A User's Guide</i></div>

<br>

# What is pymata4? 

[Pymata4](https://github.com/MrYsLab/pymata4) is a Python 3 compatible (Version 3.7 or above)  [Firmata Protocol](https://github.com/firmata/protocol) 
client that, in conjunction with an Arduino Firmata sketch, permits you to control and monitor Arduino hardware
remotely over a serial link.

Like its asyncio sibling [pymata-express,](https://mryslab.github.io/pymata-express/) pymata4 allows the user to take
advantage of the advanced feature set of 
the [FirmataExpress](https://github.com/MrYsLab/FirmataExpress) (recommended) or StandardFirmata 
Arduino server sketches. 


## A summary of pymata4's major features:

* Applications are programmed using conventional Python 3.
* Data change events may be associated with a callback function for asynchronous notification, 
or polling may be used when a synchronous approach is desired.
* Each data change event is time-stamped and stored.
* [API Reference Documentation](https://htmlpreview.github.com/?https://github.com/MrYsLab/pymata4/blob/master/html/pymata4/index.html) 
 is available online.
* A full set of working examples
are available for download [online.](https://github.com/MrYsLab/pymata4/tree/master/examples)


## Advantages of Using The FirmataExpress Sketch Over StandardFirmata:

* The data link runs at 115200, twice the speed of StandardFirmata.
* Advanced Arduino auto-discovery support is provided.
* Additional hardware support is provided for:
    * HC-SR04 ultrasonic distance sensors.
    * Stepper motors.
    * Tone generation for piezo devices.
    

## An Intuitive And Easy To use API

For example, to receive asynchronous digital pin state data change notifications, you simply do the following:

1. Set a pin mode for the pin and register a callback function.
2. Have your application sit in a loop waiting for notifications.
    
When pymata4 executes your callback method, the data parameter will contain
a list of items that describe the change event, including a time-stamp.

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
```bash
Pin: 12 Value: 0 Time Stamp: 2020-03-10 13:26:22
Pin: 12 Value: 1 Time Stamp: 2020-03-10 13:26:27
```


## What You Will Find In This Document

* A discussion of the API methods including links to working examples.
* A discussion about the threading model.
* Installation and system requirements:
    * [Verifying The Python 3 Version.](./python_3_verify/#how-to-verify-the-python-3-version-installed) 
    * [Python 3 Installation Instructions.](./python_install/#installing-python-37-or-greater)
    * [Installing _pymata4_.](./install_pymata4/#before-you-install)
    * [Installing FirmataExpress On Your Arduino.](./firmata_express/#installation-instructions)


<br>
<br>

Copyright (C) 2020 Alan Yorinks. All Rights Reserved.

**Last updated 2 April 2020 For Release v1.01**
