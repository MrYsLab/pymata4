# The Pymata4 API

If you are experienced using Firmata clients, then the 
[reference API](https://htmlpreview.github.com/?https://github.com/MrYsLab/pymata4/blob/master/html/pymata4/index.html)
may be all you need to get going. However if you want some additional detail coupled with
links to working exmples, please read on.

The reference API is organized with methods arranged in alphabetical order.

In the discussions that follow, the API is organized into the 
following functional groups:

* Instantiating the Pymata4 class.
* Establishing pin modes.
* Monitoring pin state changes.
    * Callbacks
    * Polling
* Requesting Report Information.
* Performing Management Functions.


## Instantiating The Pymata4 Class

If you are using FiramataExpress with a single Arduino, then in most cases, you
 can accept all of the default parameters provided in the \__init__ method.
 
But there are times when you may wish to take advantage of the flexibility provided
by the \__init__ method parameters, so let's explore the definition and purpose
of each parameter:

```python
def __init__(self, com_port=None, baud_rate=115200,
                 arduino_instance_id=1, arduino_wait=4,
                 sleep_tune=0.000001,
                 shutdown_on_exception=True):
```

## The Auto-Discovery Parameters - com_port, baud_rate, and arduino_instance
By accepting the default values for these parameters, pymata4 assumes you have
flashed your Arduino with FirmataExpress. 

Let's explore each parameter's function.

### com_port
The *com_port* parameter specifies a serial com_port, such as COM4 or '/dev/ttyACM0'
 used for PC to Arduino communication. If the default value of _None_ is accepted,
 pymata4 will attempt to find the connected Arduino automatically.
 
### baud_rate
The default for this parameter is 115200, matching the speed set in the 
FirmataExpress sketch. If you wish to use StandardFirmata instead of
FirmataExpress, you will set the baud_rate to 57600. If you specify the baud_rate
and accept the default com_port value, pymata4 attempts to find a connected Arduino
Instantiating The Pymata4 Class

If you are using FiramataExpress with a single Arduino, then in most cases, you can accept all of the default parameters provided in the __init__ method.

But there are times when you may wish to take advantage of the flexibility provided by the __init__ method parameters, so let's explore the definition and purpose of each parameter:

def __init__(self, com_port=None, baud_rate=115200,
                 arduino_instance_id=1, arduino_wait=4,
                 sleep_tune=0.000001,
                 shutdown_on_exception=True):

The Auto-Discovery Parameters - com_port, baud_rate, and arduino_instance

By accepting the default values for these parameters, pymata4 assumes you have flashed your Arduino with FirmataExpress.

### arduino_instance_id
This parameter is only valid when using FirmataExpress. This parameter
allows pymata4 to match a specific com_port with a specific Arduino.
The default value for the arduino_instance_id for both pymata4 and FirmataExpress is 1.
To allow pymata4 to auto-discover a com_port for a specific connected Arduino, the
arduino_instance_id values in both the FirmataExpress and pymata4 must match.
Instructions for changing the FirmataExpress value may be found
in the **Installing FirmataExpress** section of this document.

## arduino_wait
This parameter specifies the amount of time that pymata4 assumes it takes for an Arduino 
to reboot FirmataExpress (or StandardFirmata) sketch from a power-up or reset.

The default is 4 seconds. If the Arduino is not fully booted when com_port auto-discovery begins,
it will fail.

## sleep_tune
This is the sleep value expressed in seconds that is used at several strategic
points in pymata4. For example, the serial received thread continuously checks if a 
character is available to be received from the Arduino. If there is no character in the
buffer, this thread sleeps for the sleep_tune value before checking again.

## shutdown_on_exception
The default value is True. When an exception occurs within pymata4,
the shutdown method is called to perform an orderly shutdown. If you set
this to False, the exception is raised without calling shutdown.

By setting this parameter to False, the Arduino will remain in its current state. 
In contrast, when it is set to True, the Arduino will be set to a known, and hopefully safe state.

## Exceptions
Pymata4 will raise a RuntimeError exception in \__init__ for the following reasons:

1. Python version being using is not Python 3.7 or higher.
2. Auto-discovery fails for any reason.
3. The user hit Control-C.
<br>
<br>


Copyright (C) 2019-2020 Alan Yorinks. All Rights Reserved.