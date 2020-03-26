# Remote Firmata Management

## keep_alive

This is a FirmataExpress feature. If you are using an Arduino
with an Arduino that uses an ATmega328P processor, if serial communication
is lost between pymata4 and the Arduino, the Arduino will perform 
a hardware reset of itself.

```python
 def keep_alive(self, period=1, margin=0.3)

    This is a FirmataExpress feature.

    Periodically send a keep alive message to the Arduino.

    If the Arduino does not received a keep alive, the 
    Arduino will physically reset itself.

    Frequency of keep alive transmission is calculated as follows: 
        keep_alive_sent = period - (period * margin)

    :param period: Time period between keepalives. Range is 0-10 seconds. 
                   0 disables the keepalive mechanism.

    :param margin: Safety margin to assure keepalives are 
                   sent before period expires. Range is 0.1 to 0.9 
```

**Example:**

[keep_alive.py](https://github.com/MrYsLab/pymata4/blob/master/examples/keep_alive.py)

## send_reset

```python
 def send_reset(self)

    Send a Sysex reset command to the arduino
```

**Example:**

[send_reset.py](https://github.com/MrYsLab/pymata4/blob/master/examples/keep_alive.py)

**Notes:**

This command will reset several Firmata internal data structures. 

* It resets its internal i2c flags to indicate there are no i2c devices present.
* Digital reporting is turned off.
* It resets any analog pin that was set to a digital mode back to analog mode.
* If a pin was configured for tone, the tone is turned off.
* It clears all servo entries from its servo map.
* It sets the number of active sonar devices to zero.

<br>
<br>

Copyright (C) 2020 Alan Yorinks. All Rights Reserved.
