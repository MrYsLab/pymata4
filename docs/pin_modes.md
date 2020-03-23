# Introduction
Arduino pins can be configured to work in a variety of ways. For example,
a digital pin may be configured to act as either an input or an output. Analog input pins
are even more flexible.
They may be configured to act as an analog input, digital input or digital output.

Before looking at the specific pin mode methods and how to use them, 
let's discuss Arduino pin modes in a little more detail.

## Digital Pin Modes

**NOTE:**  The Arduino terminology, in my opinion, can be confusing when discussing PWM
functionality. In Arduino terminology, the function  to perform a *write* on a PWM pin is *analog_write*.
However there are Arduino boards available that have true Digital To Analog Converters, and
as a result, the term *analog* is ambiguous. To keep the terminology explicit, 
pymata4 refers to PWM operations using PWM in the method's name.


### __set_pin_mode_digital_input__

method signature

__set_pin_mode_digital_input_pullup__

__set_pin_mode_digital_output__

__set_pin_mode_pwm_output__





Currently the Firmata protocol does not support DAC operations, but if it does in the future,
pymata4 can be easily enhanced to support true DAC and continue to be explicit in its
terminology.

## Analog Pins

When using the standard Arduino C++ API to differentiate analog from digital pins, an analog pin 
is specified by using the letter "A" prefixing the pin number.

With pymata4, such a distinction is not necessary because 
the pymata4 methods that address analog functionality all contain the word
"analog" in their names.

As a result, to specify an analog pin number, you only use the numeric portion 
of the pin name. For example, if you wish to refer to analog input pin 3 (A3), with
pymata4, it is simply referred to as 3. This simplifies parsing pin numbers when your
application receives data change notifications for the pin.


* __set_pin_mode_analog_input__
* __analog_read__
* __disable_analog_reporting__
* __enable_analog_reporting__



# Pymata4 Mode Types
Pymata4 separates modes into two classifications. The first set are the pin modes,
and the second are device modes, for items such as a servo or stepper motor.

Before using a pin or device, pymata4 requires that the application explicitly
sets the desired mode. 

##  Setting Pin Modes

### set_pin_mode_analog_input

### set_pin_mode_digital_input

### set_pin_mode_digital_input_pullup

### set_pin_mode_digital_output

### set_pin_mode_pwm_output

## Setting Device Modes

### set_pin_mode_i2c

### set_pin_mode_servo

### set_pin_mode_sonar

### set_pin_mode_stepper

### set_pin_mode_tone





<br>
<br>

Copyright (C) 2020 Alan Yorinks. All Rights Reserved.
