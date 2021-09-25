import serial
from input import *
import time
import os


data_buf = []

def get_size():
    size=os.path.getsize("App.bin")
    return size

def word_to_byte(addr, index , lowerfirst):
    value = (addr >> ( 8 * ( index -1)) & 0x000000FF )
    return value

def mem_flash():
    data_file=open("App.bin","rb")
    remaining_bytes=get_size(data_file)
    data_to_read=0
    packet_length=0
    while(remaining_bytes!=0):
        if(remaining_bytes < 128):
            data_to_read=remaining_bytes
        else:
            data_to_read =128
        packet_length=data_to_read+4+4 #mem address + CRC + datalength + data
        data_buf[0]=word_to_byte(mem_address,1,1)
        data_buf[1]=word_to_byte(mem_address,2,1)
        data_buf[2]=word_to_byte(mem_address,3,1)
        data_buf[3]=word_to_byte(mem_address,4,1)
        data_buf[4]=word_to_byte(CRC,1,1)
        data_buf[5]=word_to_byte(CRC,2,1)
        data_buf[6]=word_to_byte(CRC,3,1)
        data_buf[7]=word_to_byte(CRC,4,1)
        





""""
str=b'\xa79Nz'
f=open("C:/Users/T470S/Desktop/Bootloader/App.bin","rb" )
print(f.read())
#print(str.decode())
"""

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
