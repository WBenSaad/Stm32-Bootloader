import argparse
import os
import serial


prefix="serial."

def parseCommandLineArguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--address",required=True,
                              help="specify Port Name")
    ap.add_argument("-p", "--Port", required=True,
                              help="specify Port Name")
    ap.add_argument("-b", "--Baud", type=int,required=True,
                              help="Specify Baud rate")
    ap.add_argument("-t", "--timeout", type=float,
                              help="Connexion Timeout")
    ap.add_argument("-d", "--ByteSize",default="EIGHTBITS",choices=['FIVEBITS','SIXBITS','SEVENBITS','EIGHTBITS'],
                              help="Specify the Data bits number")
    ap.add_argument("-s", "--StopBits", default="STOPBITS_ONE",choices=['STOPBITS_ONE','STOPBITS_ONE_POINT_FIVE','STOPBITS_TWO'],
                              help="StopBits Value")
    ap.add_argument("-pa", "--parity", default="PARITY_NONE",choices=['PARITY_NONE','PARITY_EVEN','PARITY_ODD','PARITY_MARK','PARITY_SPACE'],
                              help="Set up the Parity Bit")
    ap.add_argument("-f", "--FlowControl", type=bool, default=False,
                              help="StopBits Value")
    args = vars(ap.parse_args())

    Port = args["Port"]
    BaudRate = args["Baud"]
    Timeout = args["timeout"]
    ByteSize = args["ByteSize"]
    Stop= args["StopBits"]
    Parity= args["parity"]
    FlowC=args["FlowControl"]
    address=args["address"]

    return address,Port,BaudRate,Timeout,ByteSize,Stop,Parity,FlowC


