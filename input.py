import argparse
import os
import serial


prefix="serial."

def parseCommandLineArguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--Filename",required=True,
                              )
    ap.add_argument("-p", "--Port", required=True,
                              )
    ap.add_argument("-b", "--Baud", type=int,required=True,
                              )
    ap.add_argument("-t", "--timeout", type=float,
                              )
    ap.add_argument("-d", "--ByteSize",default="EIGHTBITS",choices=['FIVEBITS','SIXBITS','SEVENBITS','EIGHTBITS'],
                              )
    ap.add_argument("-s", "--StopBits", default="STOPBITS_ONE",choices=['STOPBITS_ONE','STOPBITS_ONE_POINT_FIVE','STOPBITS_TWO'],
                              )
    ap.add_argument("-pa", "--parity", default="PARITY_NONE",choices=['PARITY_NONE','PARITY_EVEN','PARITY_ODD','PARITY_MARK','PARITY_SPACE'],
                              )
    ap.add_argument("-f", "--FlowControl", type=bool, default=False,
                              )
    args = vars(ap.parse_args())

    Filename = args["Filename"]
    Port = args["Port"]
    BaudRate = args["Baud"]
    Timeout = args["timeout"]
    ByteSize = args["ByteSize"]
    Stop= args["StopBits"]
    Parity= args["parity"]
    FlowC=args["FlowControl"]

    return Filename,Port,BaudRate,Timeout,ByteSize,Stop,Parity,FlowC


