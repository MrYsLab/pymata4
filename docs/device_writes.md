# Setting Pin and Device Values
In this section, we discuss writing data to:

* Digital pins.
* PWM pins.
* Piezo tone devices.
* Servo motors.
* Stepper motors.

**Note:** I2C devices are discussed in the [next section](/i2c)
 of this guide. 

## digital_write
```python
 def digital_write(self, pin, value)

    Set the specified pin to the specified value.

    :param pin: arduino pin number

    :param value: pin value (1 or 0)

```
**Example:**

1. [digital_output.py](https://github.com/MrYsLab/pymata4/blob/master/examples/digital_output.py) 


## pwm_write
```python
 def pwm_write(self, pin, value)

    Set the selected pwm pin to the specified value.

    :param pin: PWM pin number

    :param value: Pin value (0 - 0x4000)
```

**Example:**

1. [pwm_analog_output.py](https://github.com/MrYsLab/pymata4/blob/master/examples/pwm_analog_output.py) 

**Notes:** 

The value parameter is typically set between 0 and 255.

## play_tone
```python
 def play_tone(self, pin_number, frequency, duration)

    This is FirmataExpress feature

    Play a tone at the specified frequency for the specified duration.

    :param pin_number: arduino pin number

    :param frequency: tone frequency in hz

    :param duration: duration in milliseconds

```
**Example:**

1. [play_tone.py](https://github.com/MrYsLab/pymata4/blob/master/examples/play_tone.py) 

## play_tone_continuously
```python
 def play_tone_continuously(self, pin_number, frequency)

    This is a FirmataExpress feature

    This method plays a tone continuously until play_tone_off is called.

    :param pin_number: arduino pin number

    :param frequency: tone frequency in hz
```
**Example:**

1. [play_tone.py](https://github.com/MrYsLab/pymata4/blob/master/examples/play_tone.py) 

## play_tone_off
```python
 def play_tone_off(self, pin_number)

    This is a FirmataExpress Feature

    This method turns tone off for the specified pin. 

    :param pin_number: arduino pin number
```

**Example:**

1. [play_tone.py](https://github.com/MrYsLab/pymata4/blob/master/examples/play_tone.py) 

## servo_write
```python
 def servo_write(self, pin, position)

    This is an alias for analog_write to set the position of a servo that has 
    been previously configured using set_pin_mode_servo.

    :param pin: arduino pin number

    :param position: servo position
```
**Example:**

1. [servo.py](https://github.com/MrYsLab/pymata4/blob/master/examples/servo.py) 

**Notes:** 

For an angular servo, the position parameter is set between 0 and 180 (degrees).
For a continuous servo, 0 is full-speed in one direction, 
180 is full speed in the other, and a value near 90 is no movement.

## stepper_write
```python
 def stepper_write(self, motor_speed, number_of_steps)

    This is a FirmataExpress feature

    Move a stepper motor for the number of steps at the specified speed.

    :param motor_speed: 21 bits of data to set motor speed

    :param number_of_steps: 14 bits for number of steps & direction positive is forward, negative is reverse

```
**Example:**

1. [stepper.py](https://github.com/MrYsLab/pymata4/blob/master/examples/stepper.py) 

<br>
<br>

Copyright (C) 2020 Alan Yorinks. All Rights Reserved.
