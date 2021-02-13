
        ******* USE AT YOUR OWN RISK *******

        ******* BACK UP YOUR IC-7300 *******

        *******  NO SUPPORT OFFERED  *******


ic-keyswitch was written solely as an educational venture during the COVID-19
pandemic of 2020.

The original purpose of the program was to make it easy to switch between 
paddles and straight key or (real) bug on the 7300, since their menu is 
cumbersome for doing that.

This program works with the firmware version 1.3.  It might work with 
the older one, but not tested.

This program is optimized to use Python v3.  It will likely not run at all
under version 2 of Python.  Any version 3.5.6 or better should work.

This program does not pipe audio in either direction, just does the 
CI-V back and forth from the radio.

This program does work on the Raspberry Pi 3 and 4.

This program also works in "regular" Linux.

The code is sloppy and experimental, and is not a "professional" product.

Before running this program, be sure the below statements work with
your Python > 3.5.6 interpreter on your system:

import serial.tools.list_ports
from time import sleep
from tkinter import *
import xmlrpc.client
import serial
import socket
import sys

After you verify that, the USB port on Linux (to which your radio is hooked) 
may be something like /dev/ttyUSB0.


