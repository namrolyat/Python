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

level_mode = bytearray([0, 2, 255])
trigger_mode = bytearray([0,2,0])
pulse_mode = bytearray([0,1])
values = bytearray()

try: 
    ser.open()
except Exception as e2:
    print ("error open serial port: ") + str(e2)
    exit()

if ser.isOpen():

    try:
        time.sleep(3)
        ser.flushInput()     #flush input buffer, discarding all its contents
        ser.flushOutput()    #flush output buffer, aborting current output 
                             #and discard all that is in buffer
        time.sleep(1)
        stop = 1
        while stop > 0:
            print("1: Set to levelmode.")
            print("2: Set to Trigger mode.")
            print("3: Set to pulse length mode.")
            print("4: Enter byte to be send.")
            print("0: Quit program.\n")
            
            menu_option = input("Take a pick from the main menu: ")
            print("Your pick is: " + str(menu_option) )
            if menu_option == "1":
                print("Set Bitsi to level mode.\n")
                ser.write(level_mode)
                #x = int(input('please enter an integer') )
                #print("Integer is: " + str(x) )
            elif menu_option == "2":
                print("Set Bitsi to trigger mode.\n")
                ser.write(trigger_mode)
            elif menu_option == "3":
                print("Set Bitsi to pulse mode.\n")
                ser.write(pulse_mode)
                i = int(input("Enter the time in ms for the pulse length.\n"))
                print("\nYou entered: " + str(i) + "ms\n")
                #b = i.to_bytes(2, byteorder = 'big') 
                #b = i.to_bytes((i.bit_length() // 8) + 1, byteorder='big', signed = False) #works till 127
                my_byte = b"%x" % i  #error namme 'b' is not defined
                print (my_byte)
                ser.write(my_byte)
            elif menu_option == "4":
                out = 1
                while out > 0:
                    inchar = input("Enter the byte to be send.\n")
                    print("\nYou entered: " + inchar + "\n")
                    if inchar == "q":
                        out = 0
                    else: 
                        my_int = int(inchar)
                        #my_byte = b"%x" % my_int #prints ok but writes ascii
                        #my_byte = my_int.to_bytes((my_int.bit_length() // 8) + 1, byteorder='big', signed = False)
                        my_byte = (my_int).to_bytes(1,'big')
                        
                        print(my_byte)
                        print("\n")
                        ser.write(my_byte)
            elif menu_option == "0":
                print("Trigger mode will be selected and the program will close.\n")
                stop = 0


        ser.write(trigger_mode)
        time.sleep(1)

        ser.write(trigger_mode)
        time.sleep(1)
        
        ser.close()
       
    except Exception as e1:
        print ("error communicating...: ")
        print(e1)

else:
    print ("cannot open serial port ")
	
#from: https://stackoverflow.com/questions/676172/full-examples-of-using-pyserial-package
#https://www.raspberrypi.org/forums/viewtopic.php?t=197801
#https://stackoverflow.com/questions/21017698/converting-int-to-bytes-in-python-3   
#https://www.python.org/dev/peps/pep-0461/
