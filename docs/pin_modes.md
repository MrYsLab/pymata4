# Introduction
An Arduino pin can be configured to operate in one of several modes.
The modes available to any given pin is dependent upon pin type.

For example, 
a digital pin may be configured for input, output, and for some digital pins, PWM output operation.

Analog input pins
are even more flexible.
They may be configured for analog input, digital input, or digital output operation.

Pymata4 requires that before using a pin, its mode must be explicitly set. This is accomplished using one of
the pymata4 mode setting methods.

In this section, the methods to set pin modes are presented. For each API method, a link to an example is
provided. 

## ANALOG PIN MODE

### set_pin_mode_analog_input

```python
 def set_pin_mode_analog_input(self, pin_number, callback=None, differential=1)

    Set a pin as an analog input.

    :param pin_number: arduino pin number

    :param callback: callback function

    :param differential: This value needs to be met for a callback to be invoked.

    callback returns a data list:

    [pin_type, pin_number, pin_value, raw_time_stamp]

    The pin_type for analog input pins = 2
```
**Examples:**

1. [analog_input_with_time_stamps.py](https://github.com/MrYsLab/pymata4/blob/master/examples/analog_input_with_time_stamps.py)
2. [analog_input_with_time_stamps_oo.py](https://github.com/MrYsLab/pymata4/blob/master/examples/analog_input_with_time_stamps_oo.py)

**Notes:** 

1. When an analog input message is received from Firmata, the current reported
data value is compared with that of the previously reported value. If the difference, either positive or negative,
is greater than the differential parameter, then the callback is invoked. This is useful when you have a "noisy"
input that may constantly fluctuate by a small value, and you wish to ignore the noise.
2. Pymata4 refers to analog pins using the numeric portion of the pin number only. 
For example, pin A3 is referred to as pin 3.
3. Data reporting via callbacks for this pin begins immediately after this method is called. 



## DIGITAL PIN MODES

### set_pin_mode_digital_input
```python
 def set_pin_mode_digital_input(self, pin_number, callback=None)

    Set a pin as a digital input.

    :param pin_number: arduino pin number

    :param callback: callback function

    callback returns a data list:

    [pin_type, pin_number, pin_value, raw_time_stamp]

    The pin_type for digital input pins = 0
```

**Examples:** 

1. [digital_input.py](https://github.com/MrYsLab/pymata4/blob/master/examples/digital_input.py)
2. [digital_input_debounce.py](https://github.com/MrYsLab/pymata4/blob/master/examples/digital_input_debounce.py)

**Notes:** 

Data reporting via callbacks for this pin begins immediately after this method is called. 


### set_pin_mode_digital_input_pullup

```python
 def set_pin_mode_digital_input_pullup(self, pin_number, callback=None)

    Set a pin as a digital input with pullup enabled.

    :param pin_number: arduino pin number

    :param callback: callback function

    callback returns a data list:

    [pin_type, pin_number, pin_value, raw_time_stamp]

    The pin_type for digital input pins with pullups enabled = 11

```
**Example:** 

1. [digital_input_pullup.py](https://github.com/MrYsLab/pymata4/blob/master/examples/digital_input_pullup.py) 

**Notes:** 

Data reporting via callbacks for this pin begins immediately after this method is called. 

### set_pin_mode_digital_output
```python
 def set_pin_mode_digital_output(self, pin_number)

    Set a pin as a digital output pin.

    :param pin_number: arduino pin number

```
**Examples:** 
1. [digital_output.py](https://github.com/MrYsLab/pymata4/blob/master/examples/digital_output.py)
2. [digital_pin_output.py](https://github.com/MrYsLab/pymata4/blob/master/examples/digital_pin_output.py)


### set_pin_mode_pwm_output

```python
 def set_pin_mode_pwm_output(self, pin_number)

    Set a pin as a pwm (analog output) pin.

    :param pin_number:arduino pin number
```

**Example:**
1. [pwm_analog_output.py](https://github.com/MrYsLab/pymata4/blob/master/examples/pwm_analog_output.py)

**Notes:** 

Only specific digital pins support PWM mode. Check with the Arduino documentation
to determine which pins support PWM for your board.

## DEVICE TYPE PIN MODES

### set_pin_mode_i2c
```python
def set_pin_mode_i2c(self, read_delay_time=0)

    Establish the standard Arduino i2c pins for i2c utilization.

    NOTE: THIS METHOD MUST BE CALLED BEFORE ANY I2C REQUEST IS MADE:
          This method initializes Firmata for I2c operations.

    :param read_delay_time (in microseconds): an optional parameter, default is 0

    NOTE: Callbacks are set within the individual i2c read methods of this API. 
          See i2c_read, i2c_read_continuous, or i2c_read_restart_transmission.
```

**Example:**
1. [i2c_adxl345_accelerometer.py](https://github.com/MrYsLab/pymata4/blob/master/examples/i2c_adxl345_accelerometer.py)

### set_pin_mode_servo
```python
 def set_pin_mode_servo(self, pin, min_pulse=544, max_pulse=2400)

    Configure a pin as a servo pin. Set pulse min, max in ms.

    :param pin: Servo Pin.

    :param min_pulse: Min pulse width in ms.

    :param max_pulse: Max pulse width in ms.
```
**Example:**
1. [servo.py](https://github.com/MrYsLab/pymata4/blob/master/examples/servo.py)

### set_pin_mode_sonar
```python
 def set_pin_mode_sonar(self, trigger_pin, echo_pin, callback=None, timeout=80000)

    This is a FirmataExpress feature.

    Configure the pins,ping interval and maximum distance for 
    an HC-SR04 type device.

    Up to a maximum of 6 SONAR devices is supported. 
    If the maximum is exceeded a message is sent to the console and 
    the request is ignored.

    NOTE: data is measured in centimeters. Callback is 
    called only when the the latest value received is different than the previous.

    :param trigger_pin: The pin number of for the trigger (transmitter).

    :param echo_pin: The pin number for the received echo.

    :param cb: optional callback function to report sonar data changes

    :param timeout: a tuning parameter. 80000UL equals 80ms.

    callback returns a data list:

    [pin_type, trigger_pin_number, distance_value (in cm), raw_time_stamp]

    The pin_type for sonar pins = 12

```
**Example:**
1. [hc-sr04_distance_sensor.py](https://github.com/MrYsLab/pymata4/blob/master/examples/hc-sr04_distance_sensor.py)

### set_pin_mode_stepper
```python
 def set_pin_mode_stepper(self, steps_per_revolution, stepper_pins)

    This is a FirmataExpress feature.

    Configure stepper motor prior to operation. 

    :param steps_per_revolution: number of steps per motor revolution

    :param stepper_pins: a list of control pin numbers - either 4 or 2 pins
```
**Example:**
1. [stepper.py](https://github.com/MrYsLab/pymata4/blob/master/examples/stepper.py)

** Notes:**
Only a single stepper motor is supported.

### set_pin_mode_tone
```python
 def set_pin_mode_tone(self, pin_number)

    This is a FirmataExpress feature.

    Set a PWM pin to tone mode.

    :param pin_number: arduino pin number
``` 
**Example:**
1. [play_tone.py](https://github.com/MrYsLab/pymata4/blob/master/examples/play_tone.py)



<br>
<br>

Copyright (C) 2020 Alan Yorinks. All Rights Reserved.
