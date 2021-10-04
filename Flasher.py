import serial
from input import *
import os
import struct


Bootloader_Flash                        =0x01

data_buf = []

Crc = 0xFFFFFFFF

CRC_TABLE = (0x00000000, 0x04C11DB7, 0x09823B6E, 0x0D4326D9,
             0x130476DC, 0x17C56B6B, 0x1A864DB2, 0x1E475005,
             0x2608EDB8, 0x22C9F00F, 0x2F8AD6D6, 0x2B4BCB61,
             0x350C9B64, 0x31CD86D3, 0x3C8EA00A, 0x384FBDBD)


def get_size():
    size=os.path.getsize("App.bin")
    return size

def dword(value):
    return value & 0xFFFFFFFF

def crc32_fast(crc, data):
    crc, data = dword(crc), dword(data)
    crc ^= data
    for _ in range(8):
        crc = dword(crc << 4) ^ CRC_TABLE[crc >> 28]
    return crc

def crc32_fast_bytes(crc, bytes_data):
    if len(bytes_data) & 3:
        raise ValueError('bytes_data length must be multiple of four')
    for index in range(0, len(bytes_data)-4, 4):
        data = int.from_bytes(bytes_data[index : index + 4], 'little')
        crc = crc32_fast(crc, data)
    return crc


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

    print("\n   Command == > BL_MEM_WRITE")
    bytes_remaining=0
    t_len_of_file=0
    bytes_so_far_sent = 0
    len_to_read=0
    base_mem_address=0

    for i in range(132):    ### Initializing the Buffer
        data_buf.append(0)

    bin_file=open("App.bin","rb")

        #First get the total number of bytes in the .bin file.
    t_len_of_file =get_size()


    bytes_remaining = t_len_of_file - bytes_so_far_sent

     #notify bootloader flashing

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
            data_buf[x]= int(file_read_value[0])
            
             


        #data_buf[0] = len_to_read

            #/*((4 byte mem base address + 1 byte payload len)) + len_to_read is amount of bytes read from file
            #*                                      + 4 byte CRC
            # TO simplify Things we will just Send Data + 4bytes CRC
            #*/
        mem_write_cmd_total_len = 4+len_to_read  #Total Packet contains Data bytes +4 Bytes CRC

            #first field is "len_to_follow"
            #data_buf[0] =mem_write_cmd_total_len-1
        
        crc32= crc32_fast_bytes(0xFFFFFFFF,data_buf)
        
        data_buf[len_to_read]   = word_to_byte(crc32,1,1)
        data_buf[1+len_to_read] = word_to_byte(crc32,2,1)
        data_buf[2+len_to_read] = word_to_byte(crc32,3,1)
        data_buf[3+len_to_read] = word_to_byte(crc32,4,1)

            #update base mem address for the next loop
        #base_mem_address+=len_to_read

        #Notify the Bootloader of flashing
        Write_to_serial_port(Bootloader_Flash,1)    
         #Prompts Bootloader to Enter the Flash sequence
        Write_to_serial_port(mem_write_cmd_total_len,1) #Notify Bootloader of upcoming Packet size
        print(mem_write_cmd_total_len)
        
        for i in data_buf[0:mem_write_cmd_total_len]:  ## Data starts from index 0
            Write_to_serial_port(i,mem_write_cmd_total_len-1)

        ack=read_serial_port(1)
        #ack=b'0'
        if(ack.decode() == 0): 
            while(ack.decode()==0):
                for i in data_buf[0:mem_write_cmd_total_len]:  ## Data starts from index 0
                    Write_to_serial_port(i,mem_write_cmd_total_len-1)
                ack=read_serial_port(1)             
        elif(ack.decode()==1):
            break
        
        print(data_buf)
        bytes_so_far_sent+=len_to_read
        bytes_remaining = t_len_of_file - bytes_so_far_sent
        print("\n   bytes_so_far_sent:{0} -- bytes_remaining:{1}\n".format(bytes_so_far_sent,bytes_remaining)) 

        
    mem_write_active=0
    Write_to_serial_port(9,1)

########################################################################################################


base_mem_address,Port,BaudRate,Timeout,ByteSize,Stop,Parity,FlowChart =parseCommandLineArguments()



ByteSize = getattr(serial, ByteSize)
Stop = getattr(serial, Stop)
Parity = getattr(serial, Parity)


ser=serial.Serial(Port,BaudRate,bytesize=ByteSize,parity=Parity,stopbits=Stop,write_timeout = 1,timeout=None,xonxoff=FlowChart)

ser.close()

if ser.is_open==False :
    ser.open()

else: 
    print("Port already open")
mem_flash()
#str="0x1"
#Write_to_serial_port(0x1,1)


#ser.write(str.encode())
#nack=read_serial_port(3)
#print(nack)
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
