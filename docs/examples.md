# A WORD ABOUT UNIT TESTS

You may have noticed that this distribution does not come with a set of
unit tests.

The reason for this is simple. To truly test the Pymata Express library
requires that hardware devices be connected to the Arduino, and interaction
of Pymata Express with these devices needs to be physically observed.

Therefore, in place of the traditional unit tests, the examples provided
with the distribution act as unit tests. They interact with the hardware,
and the results of this
interaction may be easily observed and verified.

If changes need to be made to the library, the example programs will be re-run to
 ensure that the hardware and the library behave as expected.
If additional features are required in the future, additional
examples will be provided to test those new features.

# EXAMPLE APPLICATIONS

## [analog_input](https://github.com/MrYsLab/pymata-express/blob/master/examples/analog_input.py)
## [analog_output](https://github.com/MrYsLab/pymata-express/blob/master/examples/analog_output.py)
## [concurrent_tasks](https://github.com/MrYsLab/pymata-express/blob/master/examples/concurrent_tasks.py)
## [digital_input](https://github.com/MrYsLab/pymata-express/blob/master/examples/digital_input.py)
## [digital_input_pullup](https://github.com/MrYsLab/pymata-express/blob/master/examples/digital_input_pullup.py)
## [digital_output](https://github.com/MrYsLab/pymata-express/blob/master/examples/digital_output.py)
## [digital_pin_ouput](https://github.com/MrYsLab/pymata-express/blob/master/examples/digital_pin_output.py)
## [hc-sr04_distance_sensor](https://github.com/MrYsLab/pymata-express/blob/master/examples/hc-sr04_distance_sensor.py)
## [i2c_adxl345_accelerometer](https://github.com/MrYsLab/pymata-express/blob/master/examples/i2c_adxl345_accelerometer.py)
## [play_tone](https://github.com/MrYsLab/pymata-express/blob/master/examples/play_tone.py)
## [retrieve_analog_map](https://github.com/MrYsLab/pymata-express/blob/master/examples/retrieve_analog_map.py)
## [retrieve_capability_report](https://github.com/MrYsLab/pymata-express/blob/master/examples/retrieve_capability_report.py)
## [retrieve_firmware_version](https://github.com/MrYsLab/pymata-express/blob/master/examples/retrieve_firmware_version.py)
## [retrieve_pin_state](https://github.com/MrYsLab/pymata-express/blob/master/examples/retrieve_pin_state.py)
## [retrieve_protocol_version](https://github.com/MrYsLab/pymata-express/blob/master/examples/retrieve_protocol_version.py)
## [servo](https://github.com/MrYsLab/pymata-express/blob/master/examples/servo.py)
## [stepper](https://github.com/MrYsLab/pymata-express/blob/master/examples/stepper.py)

<br>
<br>
Copyright (C) 2019-2020 Alan Yorinks. All Rights Reserved.
