# API

## Callbacks
Pymata4 makes extensive use of asynchronous callbacks. If you are unfamiliar with 
the callback concept is, it is simply code that you write and then "attach" to the existing
API. Here is an example of a callback that pymata4 could use to notify an application that
the data for a given analog input pin has changed in value:

```python
def the_callback(data):
    """
    A callback function to report data changes.
    :param data: [pin, current reported value, pin_mode, timestamp]
    """
    print(f'Analog Input Callback: pin={data[0]} value={data[1]}')          
```

The callback is "attached" to pymata4 when setting the pin mode for an analog input:

def main():
```python
    pin = 2
    my_board.set_pin_mode_analog_input(pin, callback=the_callback)
```

Notice that when you "attach" a callback function to pymata4, only the name of the function
is used. There are no parenthesis used.



When pymata4 detects a change in value
> Explicit pymata4 terminology definitions will be shown in paragraphs formatted
> like this one.

The group of API categories is as follows:

* Instantiation of the pymata4 class
* Establishing a pin mode.
* Monitoring pin state changes.
    * Callbacks
    * Polling
* Requesting Report Information
* Performing Management Functions



<br>
<br>


Copyright (C) 2019-2020 Alan Yorinks. All Rights Reserved.