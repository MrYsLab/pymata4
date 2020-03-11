# THE PYMATA EXPRESS CLASS PARAMETERS

In most cases, when you create an instance of the PymataExpress
class, you can accept the default parameters offered in its
\__init__ method.

However, it is essential to understand what those parameters do so that
you can customize the behavior of the class to fit your needs best.

To aid in this discussion, here is the signature for the PymataExpress class:

```
class PymataExpress:
    """
    This class exposes and implements the PymataExpress API.
    It includes the public API methods as well as
    a set of private methods. This is an asyncio API

    """

    # noinspection PyPep8
    def __init__(self, com_port=None, baud_rate=115200,
                 arduino_instance_id=1, arduino_wait=4,
                 sleep_tune=0.0001, autostart=True,
                 loop=None, shutdown_on_exception=True):
```

## PARAMETERS: com_port and baud_rate

These 2 parameters are used in tandem to specify how Pymata Express
performs serial port connectivity and Arduino auto-discovery.

### Accepting The Default Values

By accepting the defaults, PymataExpress attempts to perform its auto-discovery
procedures to locate and connect to the Arduino using FirmataExpress features.

### Specifying The Com Port Explicitly With A Baud Rate of 115200

This configuration assumes that the FirmataExpress sketch has been uploaded
to the Arduino.

Auto-discovery is bypassed; however, the arduino_instance_id value is still
validated to match the value specified in the FirmataExpress sketch.
See the [arudino_instance_id](#parameter-arduino_instance_id) discussion below.

If the instance-id match is successful, the connection succeeds. If not, a RuntimeError
exception is raised.

### Using Firmata Sketches That Run At 57600

When using these sketches, you must specify both com_port and baud rate
explicitly. No auto-discovery is performed, and a connection will be attempted using
the values specified.

## PARAMETER: arduino_instance_id

If the baud rate is set to 115200, it is assumed that FirmataExpress
has been uploaded to the Arduino.

To verify that there is a working connection to the
Arduino, Pymata Express sends a query message to the Arduino.
The Arduino, in turn, returns its "ARDUINO INSTANCE" id number.
Pymata Express compares the 2 values, and if they match, instantiation proceeds.

If you change the value of this parameter from its default of a value of 1,
you must also modify the FirmataPlus sketch to provide a matching value.
You may find the instructions to
set the instance-id [here](https://mryslab.github.io/pymata-express/firmata_express/#setting-the-firmataexpress-instance-id).

If the baud rate is set to a value other than 115200, this parameter is ignored.

## PARAMETER: arduino_wait

This parameter is the amount of time allowed for an Arduino and the uploaded Firmata sketch to
complete its reset cycle. Adjust this parameter to a higher value
if you experience connection problems with the Arduino.
Before doing so, make sure that the serial USB cable is
connected correctly and that the com_port and baud_rate are correctly specified.

## PARAMETER: sleep_tune

In general, you should not adjust this value. The purpose of sleep_tune is to set a
very short asyncio.sleep time to allow critical portions of Pymata
Express to pass control back to the event loop.

## PARAMETER: autostart
When set to True (the default), the \__init__ method calls the
start() method automatically.

The start() method is responsible for:

* establishing a serial connection to the Arduino.
* performing pin discovery to determine the total number of digital and analog pins
supported by the connected Arduino device.
* starting a task to accept serial
reporting data
from the Arduino.

If you set this parameter to False, it allows you to determine when the
functionality listed in the previous paragraph begins.

The start() method is a non-asyncio method. If you require an asyncio
method, the start-aio() method performs the same functionality as start().

## PARAMETER: loop

If you wish to provide an asyncio event loop of your own,
you may specify it using this parameter.

## PARAMETER: shutdown_on_exception

By accepting the default of True, when Pymata Express raises a RunTimeError
exception, the shutdown() method is called. The shutdown() method stops
the asyncio event loop, disables all Arduino port reporting, and closes the serial port.

If you prefer to handle the RunTimeError exceptions totally within your
application, set this parameter to False.

# SOME APPLICATION GUIDELINES

Before examining a few of the examples in detail, let's
look at some coding guidelines you may wish to employ.

# CALLBACKS VERSUS POLLING

## Callbacks

The Arduino reports data changes
to
PymataExpress asynchronously as they occur.

For your application to receive data change notifications from the Arduino,
it must provide a callback function or method. This method is specified
 when you set the pin mode for an input type
pin. The callback function or method you create must be of async type and
must provide a *data* parameter.

```
async def the_callback(data):
    """
    A callback function to report data changes.

    :param data: [pin, current reported value, pin_mode, timestamp]
    """

    # YOUR PROCESSING CODE GOES HERE
```

The callback data parameter consists of a list of 4 items:

* The PIN number
* The reported VALUE change for that pin
* The MODE of that pin
* A TIMESTAMP when the change occurred.

Here is the callback used in the [digital_input example](https://github.com/MrYsLab/pymata-express/blob/master/examples/digital_input.py):

```
async def the_callback(data):
    """
    A callback function to report data changes.
    This will print the pin number, its reported value and
    the date and time when the change occurred

    :param data: [pin, current reported value, pin_mode, timestamp]
    """
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[3]))
    print('Pin: {} Value: {} Time Stamp: {}'.format(data[0], data[1], date))
```

Here is a sample of the output of this callback function:

```
Pin: 12 Value: 1 Time Stamp: 2019-01-12 10:30:23
```


When the value change notification is sent from the Arduino, this function
will print the pin number, value change, and the time that the change occurred in
a human readable format.

You may have one or more callback functions defined to handle the callbacks.

If you need to determine the pin mode in your callback function or method,
here is a list of mode types:

```
    INPUT   = 0x00  # pin set as input
    OUTPUT  = 0x01  # pin set as output
    ANALOG  = 0x02  # analog pin in analogInput mode
    PWM     = 0x03  # digital pin in PWM output mode
    SERVO   = 0x04  # digital pin in Servo output mode
    I2C     = 0x06  # pin included in I2C setup
    STEPPER = 0x08  # any pin in stepper mode
    PULLUP  = 0x0b  # Any pin in pull-up mode
    SONAR   = 0x0c  # Any pin in SONAR mode
    TONE    = 0x0d  # Any pin in tone mode
```

## Polling

Using a callback is the preferred method of receiving
Arduino reporting data; however, you may optionally poll for data changes as well.
Each time a data change is reported for an input pin,
the pin, value, mode, and timestamp are stored internally within PymataExpress.
You may retrieve those values at any time using one of the *read* methods:

* analog_read
* digital_read
* digital_pin_read
* i2c_read_saved_data
* sonar_read

You may utilize both callbacks and polling within the same application.
Here is an example of utilizing a *read* method for
[digital_read.](https://github.com/MrYsLab/pymata-express/blob/9d3d7f5976e70d55d4dd9b8cf4577f4d42751bcb/examples/digital_input.py#L55)


# EXAMINING SOME OF THE EXAMPLES

To illustrate different approaches that commonly used in coding
Pymata Express applications, let's explore a few of
the [examples](https://mryslab.github.io/pymata-express/examples/)
provided with the distribution.

Before we look at the examples, let's discuss a generalized
coding template that is used by all of the examples.

## An Application Coding Template

```
import asyncio
import sys
from pymata_express.pymata_express import PymataExpress

# YOUR APPLICATION GOES HERE

# get the event loop
loop = asyncio.get_event_loop()

# instantiate pymata_express
board = PymataExpress()

try:
    # start the main function of your application
    loop.run_until_complete(YOUR_APPLICATION)
except (KeyboardInterrupt, RuntimeError):
    loop.run_until_complete(board.shutdown())
    sys.exit(0)

```

The template above provides a good starting point when developing
a Pymata Express application.

It begins by importing both *asyncio* and the *PymataExpress* class. The template
imports *sys* as well, so that *sys.exit(0)* can be called when either
the program finishes or the user presses a Control-C. This is shown at the bottom of the template.

Your application code follows the imports. Illustrations of this are covered in the examples below.

Next, the current running asyncio event loop is retrieved:

```
loop = asyncio.get_event_loop()

```

The loop is used both to start the application

```
loop.run_until_complete(YOUR_APPLICATION)
```

and to cleanly shut the application down.

```
loop.run_until_complete(board.shutdown())

```
PymataExpress is then instantiated:

```
board = PymataExpress()
```

If you are using an asyncio function or method as your program's starting point,
the function or method is wrapped in the asyncio method *run_until_complete*.


```
    loop.run_until_complete(YOUR_APPLICATION)
```

Finally, an exception handler is provided to cleanly shutdown
the program if an exception should be thrown.

```
except (KeyboardInterrupt, RuntimeError):
    loop.run_until_complete(board.shutdown())
    sys.exit(0)

```

## A Word About Calling *shutdown()*

It is considered good practice to call shutdown when exiting
your application. Shutdown not only gracefully closes the
asyncio event loop and serial port but also disables all reporting
from the Arduino.

If you have a set a pin mode to one of the input modes, the Arduino
continues to supply pin data changes even after your program
is halted. If reports are not disabled, and you restart
your application, reporting data from the previous run may still be streaming.
The unexpected data may result in an exception to be thrown.

Explicitly calling shutdown prevents this from happening.

## A Word Of Caution About Using The *asyncio.run()* Method

Python 3.7 provides a new way of starting an asyncio program using
the asyncio.run() method.

```
import asyncio

async def main():
    print('Hello ...')
    await asyncio.sleep(1)
    print('... World!')

# Python 3.7+
asyncio.run(main())

```

When using PymataExpress, you probably ***should not*** use this construct. Here is why. If
you look at [the documentation for this method](https://docs.python.org/3/library/asyncio-task.html#id3),
it explicitly states:

*This function cannot be called when another asyncio event loop is running in the same thread.*

When you instantiate the PymataExpress class, an event loop will be running — using the
the asyncio.run() method will invoke a second event loop, and your program most likely
will not run properly.

So what is the proper way to start a PymataExpress application?

Let's look at some examples.

## Calling Pymata Express Async Methods From A Non-Async Function

The simplest form of a PymataExpress application calls
PymataExpress API methods directly from the main application file.

Since the API methods are asyncio methods, we need to make the call
"asyncio" compatible from within a non-asyncio main. Let's look at
the [play_tone.py](https://github.com/MrYsLab/pymata-express/blob/master/examples/play_tone.py) example
to illustrate this.

```
import asyncio
import sys
from pymata_express.pymata_express import PymataExpress

# This is a demonstration of the tone methods

# retrieve the event loop
loop = asyncio.get_event_loop()

# instantiate pymata express
board = PymataExpress()

try:
    # set a pin's mode for tone operations
    loop.run_until_complete(board.set_pin_mode_tone(3))

    # specify pin, frequency and duration and play tone
    loop.run_until_complete(board.play_tone(3, 1000, 500))
    loop.run_until_complete(asyncio.sleep(2))

    # specify pin and frequency and play continuously
    loop.run_until_complete(board.play_tone_continuously(3, 2000))
    loop.run_until_complete(asyncio.sleep(2))

    # specify pin to turn pin off
    loop.run_until_complete(board.play_tone_off(3))

    # clean up
    loop.run_until_complete(board.shutdown())
except KeyboardInterrupt:
    loop.run_until_complete(board.shutdown())
    sys.exit(0)
```

Here we see an example of using the coding template described [above](#an-application-coding-template).

In addition there are several examples of wrapping the PymataExpress API calls
 using *loop.run_until.complete*. This allows us to directly call the PymataExpress async API
 methods.

```
loop.run_until_complete(board.play_tone(3, 1000, 500))
```

To use this method, we first needed to get the current event_loop:

```
retrieve the event loop
loop = asyncio.get_event_loop()
```

And then use the loop to call run_until_complete:

```
# set a pin's mode for tone operations
loop.run_until_complete(board.set_pin_mode_tone(3))
```

The line above sets pin 3's mode to *tone mode*.

The *loop_run_until_complete* method schedules the
method to be run. When that method completes, the next line of code
in the script executes, similar to coding a non-asyncio application.

NOTE: If the method you are calling contains a *while True:*
loop, the method never returns.

After performing several direct calls to the API, a graceful shutdown of the application
 is performed.

## Creating Your Own Asyncio Functions That Call The PymataExpress API

Another method of creating a PymataExpress application is to create
your own asyncio functions that will call the API methods within themselves.

Let's look at the [analog_input.py](https://github.com/MrYsLab/pymata-express/blob/master/examples/analog_input.py)
example to illustrate.

```
import asyncio
import sys
from pymata_express.pymata_express import PymataExpress

# Setup a pin for analog input and monitor its changes


async def the_callback(data):
    """
    A callback function to report data changes.

    :param data: [pin, current reported value, pin_mode, timestamp]
    """
    print("analog callback data: ", data[1])


async def analog_in(my_board, pin):
    """
    This function establishes the pin as an
    analog input. Any changes on this pin will
    be reported through the call back function.

    Also, the differential parameter is being used.
    The callback will only be called when there is
    a difference of 5 or more between the current and
    last value reported.

    :param my_board: a pymata_express instance
    :param pin: Arduino pin number
    """
    await my_board.set_pin_mode_analog_input(pin,
                                             callback=the_callback,
                                             differential=5)
    # run forever waiting for input changes
    while True:
        await asyncio.sleep(1)

# get the event loop
loop = asyncio.get_event_loop()

# instantiate pymata_express
board = PymataExpress()

try:
    # start the main function
    loop.run_until_complete(analog_in(board, 2))
except (KeyboardInterrupt, RuntimeError) as e:
    loop.run_until_complete(board.shutdown())
    sys.exit(0)

```

This example sets a pin to analog input mode. It provides a callback function
to handle data sent from the Arduino, and an asyncio function called *analog_in*
that forms the main asyncio body of our program.

The program begins by retrieving the event loop and then instantiates
the PymataExpress class:

```
# get the event loop
loop = asyncio.get_event_loop()

# instantiate pymata_express
board = PymataExpress()

```

Next, it invokes our *main* asyncio method, *analog_in*:

```
# start the main function
    loop.run_until_complete(analog_in(board, 2))
```

The PymataExpress instance is passed to this function as the first parameter
and the pin number we wish to use as the second parameter.

Let's look at *analog_in*:

```
async def analog_in(my_board, pin):
    """
    This function establishes the pin as an
    analog input. Any changes on this pin will
    be reported through the call back function.

    Also, the differential parameter is being used.
    The callback will only be called when there is
    difference of 5 or more between the current and
    last value reported.

    :param my_board: a pymata_express instance
    :param pin: Arduino pin number
    """
    await my_board.set_pin_mode_analog_input(pin,
                                             callback=the_callback,
                                             differential=5)
    # run forever waiting for input changes
    while True:
        await asyncio.sleep(1)
```

This method sets the pin mode for the pin we select to be
an analog input pin. We pass *set_pin_mode_analog_input*, a
PymataExpress API method, three parameters - the pin number,
a callback method, and a differential value.

### The *differential* Value Parameter

When a pin's mode is set to analog input, the Arduino immediately
begins streaming the data value for that pin. It does this continuously
whether the value changes or not.

We may wish to throttle when the callback function or method is called
by comparing the current value sent by the Arduino and the difference between the last
and the current values. If the differential threshold value is exceeded,
the callback will be invoked.

So, for example, let's say we wish only to have the callback function
invoked when there is a value difference of 5 between the latest value and the
previous one. To do so, we set the differential parameter to 5.
If the last value, for example, was 1020, the callback
will be invoked if the latest value exceeds either 1015 or 1020.

The default differential value is 1, but if you wish to receive all
streaming data, set it to 0.

### The While Loop

Notice that this program will run forever until the user
exits it by entering a Control-C on the keyboard.

The loop sleeps for one second and uses the asyncio.sleep method
to do so.

NOTE: You must use asyncio.sleep when you wish to call sleep from
within an asyncio function or method.

Since the loop does not perform any other processing, the sleep
time could be set to any value. The program ***does not***  wait
for a second to receive the next data change. The data change is reported
immediately in the callback function. The sleep just keeps the event loop
up and running, allowing all other asyncio functions to run.

### The Callback Function

This is a simple asyncio function that simply prints out the
latest data value.

## Creating An Application That Consists Of A Set Of Concurrent Tasks

One of the main reasons to use asyncio is to have the ability to build an
application requiring concurrency, simply and directly.

This is illustrated in the [concurrent_tasks.py](https://github.com/MrYsLab/pymata-express/blob/master/examples/concurrent_tasks.py)
example.

```
import asyncio

from pymata_express.pymata_express import PymataExpress


class ConcurrentTasks:
    """

    This program will run 3 concurrent asyncio tasks:
       1. Blink an LED.
       2. Blink an additional LED at a different rate than the first
       3. Read a potentiometer and set the intensity of a third LED
          scaled to the potentiometer value

    """

    def __init__(self, board):
        """
        Initialize the class
        :param board: a pymata express instance
        """

        # get the event loop
        self.loop = board.get_event_loop()

        # save the PymataExpress instance
        self.board = board

        # establish pin numbers

        # digital pins
        self.white_led = 6
        self.blue_led = 9
        self.green_led = 10

        # analog pin
        self.potentiometer = 2

        # continue with init and run using an async method
        loop.run_until_complete(self.async_init_and_run())

    async def potentiometer_change_callback(self, data):
        """
        Call back to receive potentiometer changes.
        Scale the reported value between 0 and ~127 to
        control the green led.
        :param data: [pin, current reported value, pin_mode, timestamp]
        """

        scaled_value = data[1] // 4
        await self.board.analog_write(self.green_led, scaled_value)

    async def async_init_and_run(self):
        """
        Initialize pin modes, create tasks and then run the tasks
        """

        await self.board.set_pin_mode_digital_output(self.white_led)
        await self.board.set_pin_mode_digital_output(self.blue_led)
        await self.board.set_pin_mode_pwm(self.green_led)
        await self.board.set_pin_mode_analog_input(self.potentiometer,
                                                   self.potentiometer_change_callback)

        # Create the 2 additional tasks
        white_led_task = asyncio.create_task(self.blink_led_1(self.white_led,
                                                              1))
        blue_led_task = asyncio.create_task(self.blink_led_2(self.blue_led,
                                                             .5))
        # start the 2 tasks
        await white_led_task
        await blue_led_task

    async def blink_led_1(self, pin, sleep):
        """
        This is run as a task from async_init_and_run
        :param pin: Arduino Pin Number
        :param sleep: Blink time
        """
        toggle = 0
        while True:
            await self.board.digital_pin_write(pin, toggle)
            await asyncio.sleep(sleep)
            toggle ^= 1

    async def blink_led_2(self, pin, sleep):
        """
        This is run as a task from async_init_and_run
        :param pin: Arduino Pin Number
        :param sleep: Blink time
        """
        toggle = 0
        while True:
            await self.board.digital_pin_write(pin, toggle)
            await asyncio.sleep(sleep)
            toggle ^= 1


# Retrieve the asyncio event loop - used by exception
loop = asyncio.get_event_loop()

# Instantiate PyMataExpress
my_board = PymataExpress()
try:
    # Instantiate this class, passing in the
    # PymataExpress instance.
    ConcurrentTasks(my_board)
except (KeyboardInterrupt, RuntimeError):
    # cleanup
    loop.run_until_complete(my_board.shutdown())
    print('goodbye')
```

This is a slightly more complex example in that the program uses a class to house its code.

Let's look at it in some detail:

As in the previous examples discussed, the [coding template](#an-application-coding-template)
is used as a basis.


At the top of the file, modules are imported, and the definition of the *ConcurrentTasks*
class is specified.



### ConcurrentTasks Class

```
class ConcurrentTasks:
    """

    This program will run 3 concurrent asyncio tasks:
       1. Blink an LED.
       2. Blink an additional LED at a different rate than the first
       3. Read a potentiometer and set the intensity of a third LED
          scaled to the potentiometer value

    """

    def __init__(self, board):
        """
        Initialize the class
        :param board: a pymata express instance
        """

        # get the event loop
        self.loop = board.get_event_loop()

        # save the PymataExpress instance
        self.board = board

        # establish pin numbers

        # digital pins
        self.white_led = 6
        self.blue_led = 9
        self.green_led = 10

        # analog pin
        self.potentiometer = 2

        # continue with init and run using an async method
        loop.run_until_complete(self.async_init_and_run())

    async def potentiometer_change_callback(self, data):
        """
        Call back to receive potentiometer changes.
        Scale the reported value between 0 and ~127 to
        control the green led.
        :param data: [pin, current reported value, pin_mode, timestamp]
        """

        scaled_value = data[1] // 4
        await self.board.analog_write(self.green_led, scaled_value)

    async def async_init_and_run(self):
        """
        Initialize pin modes, create tasks and then run the tasks
        """

        await self.board.set_pin_mode_digital_output(self.white_led)
        await self.board.set_pin_mode_digital_output(self.blue_led)
        await self.board.set_pin_mode_pwm(self.green_led)
        await self.board.set_pin_mode_analog_input(self.potentiometer,
                                                   self.potentiometer_change_callback)

        # Create the 2 additional tasks
        white_led_task = asyncio.create_task(self.blink_led_1(self.white_led,
                                                              1))
        blue_led_task = asyncio.create_task(self.blink_led_2(self.blue_led,
                                                             .5))
        # start the 2 tasks
        await white_led_task
        await blue_led_task

    async def blink_led_1(self, pin, sleep):
        """
        This is run as a task from async_init_and_run
        :param pin: Arduino Pin Number
        :param sleep: Blink time
        """
        toggle = 0
        while True:
            await self.board.digital_pin_write(pin, toggle)
            await asyncio.sleep(sleep)
            toggle ^= 1

    async def blink_led_2(self, pin, sleep):
        """
        This is run as a task from async_init_and_run
        :param pin: Arduino Pin Number
        :param sleep: Blink time
        """
        toggle = 0
        while True:
            await self.board.digital_pin_write(pin, toggle)
            await asyncio.sleep(sleep)
            toggle ^= 1

```

The 3 concurrent tasks are created and run within the *ConcurrentTasks* class. These tasks are:
```
       1. Blink an LED.
       2. Blink an additional LED at a different rate than the first
       3. Read a potentiometer and set the intensity of a third LED
          scaled to the potentiometer value
```

Each task is implemented as a method within the ConcurrentTasks class.

### The \__init__ Method

```
def __init__(self, board):
        """
        Initialize the class
        :param board: a pymata express instance
        """

        # get the event loop
        self.loop = board.get_event_loop()

        # save the PymataExpress instance
        self.board = board

        # establish pin numbers

        # digital pins
        self.white_led = 6
        self.blue_led = 9
        self.green_led = 10

        # analog pin
        self.potentiometer = 2

        # continue with init and run using an async method
        loop.run_until_complete(self.async_init_and_run())
```

This method accepts a PymataExpress instance to be used by the methods
within the class. It establishes names for the various pins being used and then
starts the program by calling the *async_init_and_run* method of the class.

Because *async_init_and_run* is an async method, it is wrapped
with *run_until_complete*:

```
        loop.run_until_complete(self.async_init_and_run())

```

### A Callback Method

The class contains a callback method called *potentiometer_change_callback*.:

```
   async def potentiometer_change_callback(self, data):
        """
        Call back to receive potentiometer changes.
        Scale the reported value between 0 and ~127 to
        control the green led.
        :param data: [pin, current reported value, pin_mode, timestamp]
        """

        scaled_value = data[1] // 4
        await self.board.analog_write(self.green_led, scaled_value)
```

This method receives the latest changes to the potentiometer values reported
by the Arduino. It  then scales the reported value to be between 0 and 127 so
that it can control the intensity of the green LED.

This is one of the 3 concurrent tasks that run simultaneously


###  The Two Additional Task Methods

In addition to the callback method, the class contains 2 additional methods
 that will also be invoked as
independent, concurrent tasks.
Each of these methods (*blink_led_1* and *blink_led_2*)
blink an LED at an independent rate.
These 2 tasks will run in
tandem with the callback task.


### The *Main* Method

The *main* method of this class is named *async_init_and_run*, and
it sets the pin modes for the various pins in addition to setting the
callback method for the potentiometer pin.

**NOTE:** When the callback method is passed as a parameter to
*set_pin_mode_analog_input*, only its name is used and not the parentheses.

```
await self.board.set_pin_mode_analog_input(self.potentiometer,
                                                   self.potentiometer_change_callback)
```



Next, the *blink* tasks are created. The callback task is considered part of the main
task, and so it does not have to be explicitly created and run.

The tasks are created using the asyncio *create_task* task method, and
then the tasks are started by *awaiting* each task.


```
   async def async_init_and_run(self):
        """
        Initialize pin modes, create tasks and then run the tasks
        """

        await self.board.set_pin_mode_digital_output(self.white_led)
        await self.board.set_pin_mode_digital_output(self.blue_led)
        await self.board.set_pin_mode_pwm(self.green_led)
        await self.board.set_pin_mode_analog_input(self.potentiometer,
                                                   self.potentiometer_change_callback)

        # Create the 2 additional tasks
        white_led_task = asyncio.create_task(self.blink_led_1(self.white_led,
                                                              1))
        blue_led_task = asyncio.create_task(self.blink_led_2(self.blue_led,
                                                             .5))
        # start the 2 tasks
        await white_led_task
        await blue_led_task
```
At the bottom of the file, the event loop is retrieved, and an instance of PymataExpress is
 created.
The *ConcurrentTasks* class is instantiated, passing it the PymataExpress instance.

```
# Retrieve the asyncio event loop - used by exception
loop = asyncio.get_event_loop()

# Instantiate PyMataExpress
my_board = PymataExpress()
try:
    # Instantiate this class, passing in the
    # PymataExpress instance.
    ConcurrentTasks(my_board)
except (KeyboardInterrupt, RuntimeError):
    # cleanup
    loop.run_until_complete(my_board.shutdown())
    print('goodbye')
```

The blink tasks will run forever, and whenever the Arduino sends a data change
report for the potentiometer, it will be processed as well.

This program runs very efficiently. On a Linux computer running
an Intel Core i5-2500K CPU at 3.30GHz, CPU utilization is 5%.

<br>
<br>


Copyright (C) 2019-2020 Alan Yorinks. All Rights Reserved.