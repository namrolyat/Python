# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 16:54:26 2020

@author: uriplo
Description:
    The program opens port 1 (Bitsi). If the port is already open (used by another
    program), the program exits. 
    When the port is open, is flushes both input and output and  then starts a 
    loop outputting 1 through 255 to the bitsi.
    
    Note that it is important to exclude the '0' in the loop, since it will put
    the bitsi in programming mode.
"""

import time
import serial

try:
    # configure the serial connections (the parameters differs on the device you are connecting to)
    # this configuration reflects the bitsi parameters
    ser = serial.Serial(
        port='COM1',
        baudrate=115200,
        #parity=serial.PARITY_NONE,
        #stopbits=serial.STOPBITS_ONE,
        #bytesize=serial.EIGHTBITS
    )

    if(ser.isOpen() == False):
        ser.open()

    print ("Port is opened.")
    
except Exception as e1:
    ser.close()
    print("Error opening port: ")    # + str(e1)
    print(e1)
    exit()
    
try:

    if ser.isOpen():
        ser.flushInput()
        ser.flushOutput()
        
        for Count in range (1, 255):  # do it from 1 till 254
            timeNow = time.time()     # read the time and store it in timeNow
                       
            #a_bytes_little = Count.to_bytes(1, 'little')
            #ser.write( a_bytes_little )
			ser.write(128)             # write bit 8 (B1000 0000)
            #print (a_bytes_little)     
            while time.time() < (timeNow + 0.5): # wait half a second
                pass
    ser.close()
    print("Port is closed")
    print("end.")
            
        
except Exception as e2:
    print ("Error communicating... : ")
    print (e2)
    ser.close()