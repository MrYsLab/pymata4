# REPORTING ISSUES

If you wish to report an issue with Pymata Express please use
[this link](https://github.com/MrYsLab/pymata-express/issues).
For FirmataExpress, please use [this link](https://github.com/MrYsLab/FirmataExpress/issues).

When filing an issue, please provide any console output, a description
of the issue, and a some code so that the problem can be reproduced.

If you have any questions about Pymata Express or FirmataExpress, you
may also use the issues links to do that as well.

# TROUBLESHOOTING TIPS

Powering both Arduino connected devices (such as motors) and the Arduino micro-controller
from your computer's USB connector
may exceed the maximum current capabilities of the USB port.
In those cases, use a separate power supply for the
connected device.

When insufficient power is available, you may see
an exception traceback that looks similar to the following:

```
Traceback (most recent call last):
  File "/home/afy/PycharmProjects/pymata-express/examples/pymata_express/servo.py", line 44, in <module>
    loop.run_until_complete(servo(board, 5))
  File "/usr/local/lib/python3.7/asyncio/base_events.py", line 584, in run_until_complete
    return future.result()
concurrent.futures._base.CancelledError
```

This exception was caused while operating a servo motor. Connecting an external
supply for the motor solved the issue.

<br>
<br>


Copyright (C) 2019-2020 Alan Yorinks. All Rights Reserved.