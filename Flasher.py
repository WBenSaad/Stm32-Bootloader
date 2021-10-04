import serial
from input import *
import os
import struct


Bootloader_Flash                        =0x01
Bootloader_Flash_end                    =0x09

data_buf = []

Crc = 0xFFFFFFFF

CRC_TABLE = (0x00000000, 0x04C11DB7, 0x09823B6E, 0x0D4326D9,
             0x130476DC, 0x17C56B6B, 0x1A864DB2, 0x1E475005,
             0x2608EDB8, 0x22C9F00F, 0x2F8AD6D6, 0x2B4BCB61,
             0x350C9B64, 0x31CD86D3, 0x3C8EA00A, 0x384FBDBD)



def get_size(str):
    size=os.path.getsize(str)
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


def mem_flash(str):

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
    t_len_of_file =get_size(str)


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
            
             
        mem_write_cmd_total_len = 4+len_to_read  #Total Packet contains Data bytes +4 Bytes CRC
        
        crc32= crc32_fast_bytes(0xFFFFFFFF,data_buf)
        
        data_buf[len_to_read]   = word_to_byte(crc32,1,1)
        data_buf[1+len_to_read] = word_to_byte(crc32,2,1)
        data_buf[2+len_to_read] = word_to_byte(crc32,3,1)
        data_buf[3+len_to_read] = word_to_byte(crc32,4,1)


        #Notify the Bootloader of flashing
        Write_to_serial_port(Bootloader_Flash,1)    
        
        #Notify Bootloader of upcoming Packet size
        Write_to_serial_port(mem_write_cmd_total_len,1) 
        print(mem_write_cmd_total_len)
        
        for i in data_buf[0:mem_write_cmd_total_len]:  ## Data starts from index 0
            Write_to_serial_port(i,mem_write_cmd_total_len-1)

        #The Bootloader will send a 0 if the Packet was corrupted during transmission(Having a non matching Checksum )
        #then the we will keep resending the entire packet until we get a favorable response (1) from the Bootloader

        ack=read_serial_port(1)
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
    #Notify the Bootloader that the transmission is over
    Write_to_serial_port(Bootloader_Flash_end,1)




filename,Port,BaudRate,Timeout,ByteSize,Stop,Parity,FlowChart =parseCommandLineArguments()


ByteSize = getattr(serial, ByteSize)
Stop = getattr(serial, Stop)
Parity = getattr(serial, Parity)


ser=serial.Serial(Port,BaudRate,bytesize=ByteSize,parity=Parity,stopbits=Stop,write_timeout = 1,timeout=None,xonxoff=FlowChart)

ser.close()

if ser.is_open==False :
    ser.open()

else: 
    print("Port already open")

mem_flash(filename)
