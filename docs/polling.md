# Processing Input Data

Understanding how both Firmata generates input data notification messages, as well as 
how pymata4 processes these messages, may be
beneficial in designing your application.

## Firmata Data Collection

Both the FirmataExpress and StandardFirmata sketches poll all input pins within the *loop method*
of the sketch.

Firmata builds notification messages containing the pin number, pin type, and data value,
 and these messages are sent to pymata4
over the serial link.

## Firmata Data Polling

### Digital Input
For digital input pins, all the pins are polled with *each* iteration of the loop,
with no delays. Data changes are reported by generating change notification
 messages and transmitting them over the serial link.


### Analog Input
For analog input pins, the Firmata *loop* polls and reports the current value of each pin, 
regardless of change, 
All analog input pins are nominally polled every 19 milliseconds.

### I2C Input
If you are using i2c devices that support a continuous read mode,
the Firmata *loop* polls each device. It then reports the current value of each device, regardless of change.
This is done nominally every 19 milliseconds for all i2c devices configured for
continuous read.

### Sonar (HC-SR04) Input
FirmataExpress supports HC-SR04 type distance sensors. The Firmata *loop* polls each device 
and reports its current value regardless of change.
This is done nominally every 40 milliseconds.

# Using Pymata4 To Access Input Data

## *Polling* For Input Data Changes
As pymata4 receives input data notifications, 
it caches the data in internal data structures. These structures retain
the value reported as well as a time of occurrence time-stamp.
The application may query or poll these data structures to obtain the
latest data updates for a given pin. 

The pymata4 API methods that implement polling are:

* analog_read
* digital_read
* i2c_read_saved_data
* sonar_read

A more efficient and automatic way for your application to be notified
of data updates is to use the pymata4 *callback* feature. 

## Using *Callbacks* Instead Of Polling
Callback notification is much more efficient than using polling.

A callback is simply a function or method written by you, that is called automatically
by pymata4 when it receives an input data notification message from Firmata.

You may optionally *register* callback functions when using any of the following pymata4 API
methods:

* set_pin_mode_analog_input
* set_pin_mode_digital_input
* set_pin_mode_digital_input_pullup
* set_pin_mode_sonar
* enable_analog_reporting (an alias for set_pin_mode_analog_input)
* i2c_read
* i2c_read_continuous
* i2c_read_restart_transmission

You may write a callback function for each input pin, or write
a callback function to handle any pin of single type, such as analog input
or digital input, or even have a single callback function to handle all input data notifications.

You may use callbacks with some pins while using polling for others. Polling is available
for all input pins whether callbacks are in use or not.

A callback function is specified with a single input parameter. Pymata4 passes in a list 
of information when it calls the callback function. A description of what is contained in the list
is provided in the 
[reference API.]((https://htmlpreview.github.com/?https://github.com/MrYsLab/pymata4/blob/master/html/pymata4/index.html) )

```python
def my_callback(data):
    """
    :param data: a list containing pin type, pin number, 
                 data value and time-stamp
    """
# Your code goes here to process the data
```

**TIP**: You should keep callback functions as short as possible. If processing callback
data within the callback function results in blocking your application, 
you may wish to consider spawning a separate
processing thread.


<br>
<br>

Copyright (C) 2020 Alan Yorinks. All Rights Reserved.
