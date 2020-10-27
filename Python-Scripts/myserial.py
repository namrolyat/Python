#! python

import time
import serial

try:
# configure the serial connections (the parameters differs on the device you are connecting to)
    ser = serial.Serial(
        port='COM38',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )

    if(ser.isOpen() == False):
        ser.open()

    print ("Port is opened.")

except IOError: # if port already opened, close it and open it again
    ser.close()
    ser.open()
    print ("Port was already open, was closed and opened again!")

while True:
    print ("Enter your commands below.")
    print ("Insert \'exit\' to leave the application.")


    input=1
    while 1 :
            # get keyboard input
        input = raw_input(">> ")
            # Python 3 users
            # input = input(">> ")
        if input == 'exit':
            ser.close()
            exit()
        else:
            # send the character to the device
            # (note that I appended a \r\n carriage return and line feed to the characters - this is requested by my device)
            ser.write(input + '\r\n')
            out = ''
            # let's wait one second before reading output (let's give device time to answer)
            time.sleep(1)
            while ser.inWaiting() > 0:
                out += ser.read(1)

            if out != '':
                print (">>") + out
