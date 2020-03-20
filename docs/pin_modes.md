# Introduction

Let's take a look at Arduino pin modes before discussing how they are set.

## Digital Pin Modes
An Arduino digital pin may be configured as a:

* Digital input.
* Digital input with pull-up resistor enabled.
* Digital output.
* PWM output.

> **NOTE:**  The Arduino terminology, in my opinion, can be confusing when discussing PWM
>functionaliry. In Arduino terminology, the function  to perform a *write* on a PWM pin is *analog_write*.
>However there are Arduino boards available that have true Digital To Analog Converters, and
>as a result, the term *analog* is ambiguous. To keep the terminology explicit, 
>pymata4 refers to PWM operations using PWM in the method's name:
>
> * set_pin_mode_pwm_output - to set a digital pin as PWM output pin
> * pwm_write - to set the value on the pin
>
>
>Currently Firmata does not support DAC operations, but if it does in the future,
>pymata4 can be easily enhanced.
>

## Analog Pins

Using Arduino nomenclature, an analog pin is specified by using the letter "A" prefixing the pin number.
So for example, on an Arduino Uno there are 6 *analog input* pins numbered from A0 to A5.

What this implies, is that your application will need to parse pin numbers in two different
ways, one for digital pins and one for analog pins. Pymata4 considers all pin numbers
as numerical and does not use the "A" prefix convention, but uses a numerical
value independent of pin type. This simplifies pin
number parsing for your application.

You may be wondering how pymata4 differentiates 

```python
my_board.digital_read(3)
```

To read analog input 3, the method used is _analog_read_:

```python
myboard.analog_read(3)
```

We will be covering callbacks a little further down, but if you wish to write a single callback
method to handle input pin data change notifications for both analog and digital inputs, 
the callback function is provided with the 
pin type that invoked the callback as well as the pin number. 


> To add more confusion, an analog input pin may be configured as a digital input or
>digital output pin. In that case, the pin does not use the Ax convention mentioned above, but
>the normal digital pin number. Here is a mapping of analog pin numbers (using the Arduino terminology)
>to digital pin numbers for the Arduino Uno:
> 
> 
>using 

When a data value changes on an analog pin and your application

# Pin Mode Type
In general, a pin may be set as an _input_ pin, _output_ pin or a _device-type_ pin.

Here is a list of method calls for each type. Click on the method name to see an example of its
use.

* Input Pin Modes

    | Method 	            |    Example    
    |--------------------	|:------------:	
    | [set_pin_mode_analog_input](https://github.com/MrYsLab/pymata4/blob/master/examples/analog_input_with_time_stamps.py) 
    |         19         	|   Button B   	
    |         21         	| Slide Switch 	
    
    * [set_pin_mode_analog_input](https://github.com/MrYsLab/pymata4/blob/master/examples/analog_input_with_time_stamps.py)
    * set_pin_mode_digital_input
    * set_pin_mode_digital_input_pullup

<br>
<br>

Copyright (C) 2020 Alan Yorinks. All Rights Reserved.
