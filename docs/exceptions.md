# Exceptions
When pymata4 detects an error, it raises a RuntimeError exception. The
table below shows the exception report string that is displayed on the console
when an exception is raised. A probable cause and troubleshooting tip is also provided.



|         Exception Report        	|      Probable Cause      	|  Troubleshooting 	|
|:---------------------	|:-------------	|:-----	|
| ERROR: Python 3.7 or greater <br> is required for use <br> of this program. | Unsupported version of <br> python detected| Make sure that you are using <br> Python 3.7 or greater.	|
|        No Arduino Found or <br> User Aborted Program.       	|    Com Port not found.   	|  Make sure that you have the <br> Arduino plugged in.  	|
|        Firmata Sketch Firmware Version Not Found.       	| Valid firmware version not returned.	| Make sure that you have a Firmata sketch installed on the Arduino.	|
|Analog map retrieval timed out. <br> Do you have Arduino connectivity and do you have the <br> correct Firmata sketch uploaded to the board?|  Analog report request timed out  | Self explanatory. |
| User Hit Control-C.  |  User aborted the application.  | Not Applicable.   |
| Retrieving ID From Arduino Failed.   | FirmataExpress handshake not returned.   |  Make sure that FirmataExpress was uploaded to the Arduino  |
|  Invalid Arduino identifier retrieved  | FirmataExpress and pymata4 Arduino IDs do not match.   | Verify the Arduino IDs   |
|  write fail in _send_command  |  Serial write failed.  |  Check the serial cable.  |

<br>
<br>

Copyright (C) 2020 Alan Yorinks. All Rights Reserved.
