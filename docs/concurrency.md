# The Concurrency Model

## Introduction
In this section, we discuss the concurrency model used by pymata4.

According to [Wikipedia,](https://en.wikipedia.org/wiki/Concurrency_(computer_science)) 
*"concurrency is the ability of different parts or units of a program, algorithm, or 
problem to be executed out-of-order or in partial order, without affecting the final outcome. 
This allows for parallel execution of the concurrent units, which can significantly 
improve overall speed of the execution in multi-processor and multi-core systems."*

To assure the best possible performance, pymata4 needs to do the following tasks, all at the same time:

* Accept and process API calls from the application.
    * Translate the API calls into Firmata formatted messages.
    * Transmit these messages across the serial link.
* Continuously receive data from the serial link.
    * Assure no data loss
* Decode the received data.
    * Store information in the pymata4 internal data structures.
    * Notify the application of data change notifications by calling the user-provided callback methods.

To accomplish all this, pymata4 uses the Python [threading](https://docs.python.org/3.8/library/threading.html) 
module. It breaks its tasks into three
main threads, the *Command Thread*, the *Reporter Thread*, and the *Serial Data Reciever Thread*. 

The concurrency model is depicted in the diagram below. The three threads, including the data structures used to 
provide for inter-thread communication, are contained in the rectangle with the solid border.
This rectangle constitutes the pymata4 package.

The user application is depicted on the left side of the diagram, and the Arduino containing the
Firmata sketch is shown on the right.

![](./images/threading.png)

## The Command Thread

Whenever your application makes an API method call, it is interacting directly
with the *Command Thread*. The API calls fall into two major categories, synchronous or blocking
calls and asynchronous or non-blocking calls.

### Synchronous API Method Calls
The synchronous API methods may be placed into two categories. Calls that poll
for cached data values and calls that request report generation.

#### Polling Method Calls
* read_analog
* read_digital
* i2c_read_saved_data
* sonar_read

When the application calls one of the polling methods, the *Command Thread* accesses
the pin data, i2c data, or sonar data structures. It then retrieves the current value for the item.

The polling calls are reasonably quick in that the *Command Thread* reads and returns
a value from one of the internal data structures. Only the *Command Thread* is involved
in processing polling requests.


#### Report Request Method Calls
* get_analog_map
* get_capability_report
* get_firmware_version
* get_pin_state
* get_protocol_version
* get_pymata_version

When your application requests a report:

1. A report request message is formed and sent across the serial link to the Arduino.
2. The *Command Thread* waits in a blocking loop anticipating the report reply.
3. The Arduino processes the request. It formulates a reply and sends a response over the
serial link.
4. The *Serial Data Receiver Thread* receives the reply, and places each character on the *deque* that
is shared between the *Serial Data Receiver Thread* and the *Reporter Thread*. 
5. The *Reporter Thread* decodes the reply and places the result on an internal data structure 
shared with the *Command Thread*.
6. The *Command Thread* detects that the report is available, and returns the report to the application.
At this time, the *Command Thread* is no longer blocked.

Requesting report information should only be done when necessary because
of the long blocking period of the request.

### Asynchronous API Method Calls
All other API methods calls are considered asynchronous in that they do not block.
These calls only involve the *Command Thread*. They build a Firmata message and send the
message the Arduino over the serial link.

* digital_pin_write
* digital_write
* disable_analog_reporting
* disable_digital_reporting
* enable_analog_reporting
* enable_digital_reporting
* i2c_read
* i2c_read_continuous
* i2c_read_restart_transmission
* i2c_write
* keep_alive
* play_tone
* play_tone_continuously
* play_tone_off
* pwm_write
* send_reset
* servo_write
* set_pin_mode_analog_input
* set_pin_mode_digital_input
* set_pin_mode_digital_input_pullup
* set_pin_mode_digital_output
* set_pin_mode_i2c
* set_pin_mode_pwm_output
* set_pin_mode_servo
* set_pin_mode_sonar
* set_pin_mode_stepper
* set_pin_mode_tone
* set_sampling_interval
* shutdown
* sonar_read
* stepper_write


## The Reporter Thread

The *Reporter Thread* continuously monitors the *deque* to see if any data is 
available from the Arduino to process. 

If the *Reporter Thread* receives an input data type message, it places
the latest value in one of the data structures that it shares with the *Command Thread*. Also,
the *Reporter Thread* determines if there is a registered callback method for the event. If so,
it *calls* the callback method passing in the appropriate data list.

Callback methods should be written to be as fast as possible so that the *Report Thread* is not
blocked.

## The Serial Data Receiver Thread
The *Serial Data Receiver Thread* continuously monitors the serial port for incoming data.
It receives data one character at a time and places the data into the deque that it shares with
the *Reporter Thread*. It does not interpret the data since this is the job of the *Reporter Thread*.

<br>
<br>

Copyright (C) 2020 Alan Yorinks. All Rights Reserved.
