#!/usr/bin/python

import serial, time
#initialization and open the port

#possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call

ser = serial.Serial()
ser.port = "COM1"
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
ser.timeout = None              #block read
#ser.timeout = 1                #non-block read
#ser.timeout = 2                #timeout block read
ser.xonxoff = False             #disable software flow control
ser.rtscts = False              #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False              #disable hardware (DSR/DTR) flow control
ser.writeTimeout = False        #timeout for write

sb38 = bytearray([1,19,38,0,1,53])  #bytes are represented in decimal
rb38 = bytearray([1,19,38,0,0,52])
sb39 = bytearray([1,19,39,0,1,52])
rb39 = bytearray([1,19,39,0,0,53])

try: 
    ser.open()
except Exception as e2:
    print ("error open serial port: ") + str(e2)
    exit()

if ser.isOpen():

    try:
        ser.flushInput() #flush input buffer, discarding all its contents
        ser.flushOutput()#flush output buffer, aborting current output 
        time.sleep(2)    #wait for display to settle		

        stop = 1
        while stop > 0:
            print("1: Send individual bytes.")
            print("2: Set button 38.")
            print("3: Reset button 38.")
            print("4: Set button 39.")
            print("5: Reset button 39.")
            print("0: Quit program.\n")
            menu_option = input("Take a pick from the main menu: ")
            print("Your pick is: " + str(menu_option) )
            if menu_option == "1":
                out = 1
                while out > 0:
                    inchar = input("Enter the byte to be send.\n")
                    print("\nYou entered: " + inchar + "\n")
                    if inchar == "q":
                        out = 0
                    else: 
                        my_int = int(inchar)
                        my_byte = (my_int).to_bytes(1,'big')
                        print(my_byte)
                        print("\n")
                        ser.write(my_byte)

            elif menu_option == "0":
                print("Close program.\n")
                stop = 0
            elif menu_option == "2":
                print("Set led 38")
                print(sb38)
                ser.write(sb38)
            elif menu_option == "3":
                print("Reset led 38")
                print(rb38)
                ser.write(rb38)
            elif menu_option == "4":
                print("Set led 39")
                print(sb39)
                ser.write(sb39)
            elif menu_option == "5":
                print("Reset led 39")
                print(rb39)
                ser.write(rb39)

        ser.close()
       
    except Exception as e1:
        print ("error communicating...: ")
        print(e1)

else:
    print ("cannot open serial port ")

	
#source: https://stackoverflow.com/questions/676172/full-examples-of-using-pyserial-package
