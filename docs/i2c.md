# Communicating With I2C Devices
Pymata4 has the capability to support one or more i2c devices connected
 to the i2c bus.
The API supports several i2c read methods, and a single i2c write method, described below.

***NOTE 1:*** If you do not specify a callback for any give read method, to retrieve the latest
values, you will need to use the [i2c_read_saved_data](/pin_changes/#i2c_read_saved_data) method. 
The amount of time it takes an i2c device to reply to a an i2c read varies from device to device.
Therefore it is simpler to use callbacks.

***NOTE 2:*** An example,  is provided for *i2c_read*. Callbacks for i2c_read, 

# I2c Read Methods

## i2c_read

```python
 def i2c_read(self, address, register, number_of_bytes, callback=None)

    Read the specified number of bytes from the specified 
    register for the i2c device.

    :param address: i2c device address

    :param register: i2c register

    :param number_of_bytes: number of bytes to be read

    :param callback: Optional callback function to report i2c 
                     data as a result of read command

    callback returns a data list:

    [pin_type, i2c_device_address, i2c_read_regsiter, 
     data_bytes returned, time_stamp]

    The pin_type for i2c = 6

```
### Example:

See NOTE2 above.

## i2c_read_continuous
```python
 def i2c_read_continuous(self, address, register, number_of_bytes, callback=None)

    Some i2c devices support a continuous streaming data output. 
    This command enables that mode for the device that supports continuous reads.

    :param address: i2c device address

    :param register: i2c register

    :param number_of_bytes: number of bytes to be read

    :param callback: Optional callback function to report 
                     i2c data as a result of read command

    callback returns a data list:

    [pin_type, i2c_device_address, i2c_read_regsiter, 
     data_bytes returned, time_stamp]

    The pin_type for i2c = 6

```
### Example:

See NOTE2 above.

## i2c_read_restart_transmission
```python
 def i2c_read_restart_transmission(self, address, register, number_of_bytes, callback=None)

    Read the specified number of bytes from the specified register for the i2c device. This restarts the transmission after the read. It is required for some i2c devices such as the MMA8452Q accelerometer.

    :param address: i2c device address

    :param register: i2c register

    :param number_of_bytes: number of bytes to be read

    :param callback: Optional callback function to report i2c data as a result of read command

    callback returns a data list:

    [pin_type, i2c_device_address, i2c_read_regsiter, data_bytes returned, time_stamp]

    The pin_type for i2c pins = 6
```

### Example:

See NOTE2 above.

# I2c Write Method
##
```python
 def i2c_write(self, address, args)

    Write data to an i2c device.

    :param address: i2c device address

    :param args: A variable number of bytes to be sent 
                 to the device passed in as a list
```

<br>
<br>

Copyright (C) 2020 Alan Yorinks. All Rights Reserved.
