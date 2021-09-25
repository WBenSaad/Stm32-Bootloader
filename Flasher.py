import serial
from input import *
import time
import os

str=b'\xa79Nz'
f=open("C:/Users/T470S/Desktop/Bootloader/App.bin","rb" )
print(f.read())
#print(str.decode())

Port,BaudRate,Timeout,ByteSize,Stop,Parity,FlowChart =parseCommandLineArguments()



ByteSize = getattr(serial, ByteSize)
Stop = getattr(serial, Stop)
Parity = getattr(serial, Parity)


ser=serial.Serial(Port,BaudRate,bytesize=ByteSize,parity=Parity,stopbits=Stop,write_timeout = 1,timeout=None,xonxoff=FlowChart)

ser.close()

if ser.is_open==False :
    ser.open()

else: 
    print("Port already open")
"""
while 1:
    buffer=ser.read(5)
    Dec=buffer.decode()
    if Dec=="Hello":
        print("GUCCI")
        print(buffer)
    else :
        print("NON_GUCCI")
        print(buffer)
        


ser.write(b'1')
buffer=ser.read(3)
if(buffer.decode()=="ACK"):
    print(buffer)
    
else:
    print("3asba1")

ser.write(b'9')
buffer2=ser.read(4)
if(buffer2.decode()=="NACK"):
    print(buffer2)
else:
    print("3asba2")
    """
