#!/usr/bin/python

import serial, time
#initialization and open the port

#possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call

ser = serial.Serial()
ser.port = "COM39"
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
#ser.timeout = None             #block read
ser.timeout = 1                 #non-block read
#ser.timeout = 2                #timeout block read
ser.xonxoff = False             #disable software flow control
ser.rtscts = False              #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False              #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2            #timeout for write

values = bytearray([0, 2, 255,255])
values2 = bytearray([0,2,0])
values3 = bytearray([255])
try: 
    ser.open()
except Exception as e2:
    print ("error open serial port: ") + str(e2)
    exit()

if ser.isOpen():

    try:
        ser.flushInput()     #flush input buffer, discarding all its contents
        ser.flushOutput()    #flush output buffer, aborting current output 
                             #and discard all that is in buffer
        time.sleep(5)
        ser.write(values)
        time.sleep(5)

        ser.write(values2)
        time.sleep(2)

        ser.write(values3)
        time.sleep(2)
        
        ser.close()
       
    except Exception as e1:
        print ("error communicating...: ")
        print(e1)

else:
    print ("cannot open serial port ")
	
#from: https://stackoverflow.com/questions/676172/full-examples-of-using-pyserial-package
