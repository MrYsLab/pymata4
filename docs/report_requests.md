# Informational Reports
All of the following methods are synchronous. The methods
block until they return.

## get_analog_map
```python
 def get_analog_map(self)

    This method requests a Firmata analog map 
    query and returns the results.

    :returns: An analog map response or None if a timeout occurs

```
### Example: 
1. [retrieve_analog_map.py](https://github.com/MrYsLab/pymata4/blob/master/examples/retrieve_analog_map.py)

*** NOTES: *** 
Refer to the [Firmata Protocol specification](https://github.com/firmata/protocol/blob/master/protocol.md#analog-mapping-query)
 for an explanation of the report data. 

## get_capability_report
```python
 def get_capability_report(self)

    This method requests and returns a Firmata 
    capability query report

    :returns: A capability report in the form of a list
```
### Example: 
1. [retrieve_capability_report.py](https://github.com/MrYsLab/pymata4/blob/master/examples/retrieve_capability_report.py)

*** NOTES: *** 
Refer to the [Firmata Protocol specification](https://github.com/firmata/protocol/blob/master/protocol.md#capability-query)
 for an explanation of the report data.]
 
 ## get_firmware_version
```python
  def get_firmware_version(self)

    This method retrieves the Firmata firmware version

    :returns: Firmata firmware version
```
### Example: 
1. [retrieve_firmware_version.py](https://github.com/MrYsLab/pymata4/blob/master/examples/retrieve_firmware_version.py)

*** NOTES: *** 
Refer to the [Firmata Protocol specification](https://github.com/firmata/protocol/blob/master/protocol.md#capability-query)
 for an explanation of the report data.

<br>
<br>

Copyright (C) 2020 Alan Yorinks. All Rights Reserved.
