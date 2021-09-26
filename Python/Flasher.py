import serial
from input import *
import os
import struct


data_buf = []

def get_size():
    size=os.path.getsize("App.bin")
    return size

def get_crc(buff, length):
    Crc = 0xFFFFFFFF
    #print(length)
    for data in buff[0:length]:
        Crc = Crc ^ data
        for i in range(32):
            if(Crc & 0x80000000):
                Crc = (Crc << 1) ^ 0x04C11DB7
            else:
                Crc = (Crc << 1)
    return Crc

def word_to_byte(addr, index , lowerfirst):
    value = (addr >> ( 8 * ( index -1)) & 0x000000FF )
    return value


def Write_to_serial_port(value, *length):
        data = struct.pack('>B', value)
        ser.write(data)

def read_serial_port(length):
    read_value = ser.read(length)
    return read_value


def mem_flash():
    """data_file=open("App.bin","rb")
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
        
"""
    print("\n   Command == > BL_MEM_WRITE")
    bytes_remaining=0
    t_len_of_file=0
    bytes_so_far_sent = 0
    len_to_read=0
    base_mem_address=0

    bin_file=open("App.bin","rb")

        #First get the total number of bytes in the .bin file.
    t_len_of_file =get_size(bin_file)


    bytes_remaining = t_len_of_file - bytes_so_far_sent

    global mem_write_active
    while(bytes_remaining):
        mem_write_active=1
        if(bytes_remaining >= 128):
            len_to_read = 128
        else:
            len_to_read = bytes_remaining
            #get the bytes in to buffer by reading file
        for x in range(len_to_read):
            file_read_value = bin_file.read(1)
            file_read_value = bytearray(file_read_value)
            data_buf[7+x]= int(file_read_value[0])
            #read_the_file(&data_buf[7],len_to_read) 
             

            #populate base mem address
        data_buf[0] = word_to_byte(base_mem_address,1,1)
        data_buf[1] = word_to_byte(base_mem_address,2,1)
        data_buf[2] = word_to_byte(base_mem_address,3,1)
        data_buf[3] = word_to_byte(base_mem_address,4,1)

        data_buf[4] = len_to_read

            #/*4 byte mem base address + 1 byte payload len + len_to_read is amount of bytes read from file
            #*                                      + 4 byte CRC
            #*/
        mem_write_cmd_total_len = 9+len_to_read

            #first field is "len_to_follow"
        #data_buf[0] =mem_write_cmd_total_len-1

        crc32= get_crc(data_buf,mem_write_cmd_total_len-4)
        data_buf[5+len_to_read] = word_to_byte(crc32,1,1)
        data_buf[6+len_to_read] = word_to_byte(crc32,2,1)
        data_buf[7+len_to_read] = word_to_byte(crc32,3,1)
        data_buf[8+len_to_read] = word_to_byte(crc32,4,1)

            #update base mem address for the next loop
        base_mem_address+=len_to_read

        Write_to_serial_port(data_buf[0],1)
        
        
        for i in data_buf[1:mem_write_cmd_total_len]:
            Write_to_serial_port(i,mem_write_cmd_total_len-1)

        bytes_so_far_sent+=len_to_read
        bytes_remaining = t_len_of_file - bytes_so_far_sent
        print("\n   bytes_so_far_sent:{0} -- bytes_remaining:{1}\n".format(bytes_so_far_sent,bytes_remaining)) 
        
        
    mem_write_active=0


########################################################################################################


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

Write_to_serial_port(1,1)
ack=read_serial_port(3)
print(ack)
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
