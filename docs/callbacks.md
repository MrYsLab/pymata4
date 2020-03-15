## What Is A Callback?

Pymata4 allows you to be notified of data changes using callback functions. 
A callback is simply a function or method called by pymata4 to
alert you application that a data change event has occurred. You write the callback
function as part of your application and simply register it with pymata4.

For example, if you configure a pin for analog input, when the value on that
pin changes, the associated callback function for that pin is called and your
application then provides the processing required as a result of the data change.

## Must I Use Callbacks?

Callbacks are totally optional but highly recommended.

## Why Use A Callback?

They are highly efficient. The alternative to using a callback is to peirodically poll
for data changes. To poll, your application requests the last value reported
for the reporting entity, you then must wait for the reply. Callbacks on the other
hand, once established, do not require any additional method calls by your application.
Data changes are automatically and asynchronously reported as they occur.

## How Do I Register A Callback?

You have the option to assign a callback method when a pin mode is set.
We will get into more detail a little further down in this document during the 
discussion of setting pin and operational modes.

## What Data Is Passed Back To The Callback?

A list is passed from pymata4 to the callback method. The details
of the contents of the list are discussed later during the 
discussion of setting pin and operational modes. 

## How Many Callbacks Do I Need To Write?

This is totally up to you. Within the list that pymata4 provides is an
identifier of the callback originator. This allows you to have a single 
callback function to handle all callbacks or write a callback for every
pin or callback entity. Again, the granularity is up to you and the needs
of your application.

You can also have some data changes reported via callbacks, while polling 
for others.

## Can I Still Poll For The Last Data Change?

Yes. As each data change is detected, pymata4 stores the data change with a 
timestamp. This is true if you have callbacks enabled or not. 
The API has method calls that allow you to request the latest
reported change.

<br>
<br>

Copyright (C) 2020 Alan Yorinks. All Rights Reserved.
