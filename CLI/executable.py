import IPBus
import read as read_handler
import write as write_handler
from error_codes import Error

def set_ip(*args, ipBus: IPBus.IPBus):
    if (args is None) or (len(args) == 0):
        return Error.OK, "Current IP: %s:%d" % (ipBus.address.IP, ipBus.address.port)
        
    ipBus.address.IP = args[0]

    if len(args) > 1:
        try:
            ipBus.address.port = int(args[1])
        except ValueError:
            return Error.INVALID_COMMAND, "Port must be an integer."

    return Error.OK, "IP address set to %s:%d" % (ipBus.address.IP, ipBus.address.port)

def read_status(*args, ipBus: IPBus.IPBus):
    ipBus.statusRequest()
    try:
        status = ipBus.statusResponse()
    except TimeoutError:
        return Error.TIMEOUT, "Timeout error"
    
    if status == IPBus.PacketType["status"]:
        return Error.OK, "IPBus status OK"
    
    return Error.STATUS_REQUEST, "IPBus status request failed"

def readToString(startAddress: int, data: list[int], FIFO: bool) -> str:
    string = ""

    if not FIFO:
        for i in range(len(data)):
            string += "0x%08X: 0x%08X\n" % (startAddress + i, data[i])
    else:
        string =  "0x%08X:" % startAddress
        for i in range(len(data)):
            string += " 0x%08X" % data[i]

    return string

def read(*args, ipBus: IPBus.IPBus):
    args = list(args)
    for key in read_handler.PARAMS.keys():
        if key in args:
            read_handler.PARAMS[key]["value"] = read_handler.PARAMS[key]["handler"](args)

    for i in range(len(args)):
        args[i] = int(args[i], 16)



    try: 
        status, data = ipBus.read(args[0], read_handler.PARAMS["-n"]["value"], read_handler.PARAMS["--FIFO"]["value"])
    except TimeoutError:
        return Error.TIMEOUT, "Timeout error"

    if (status != 0):
        return Error.TRANSACTION, IPBus.TransactionInfoCodeStringType[status]
    
    return Error.OK, readToString(args[0], data, read_handler.PARAMS["--FIFO"]["value"])


def write(*args, ipBus: IPBus.IPBus):
    args = list(args)

    for key in read_handler.PARAMS.keys():
        if key in args:
            write_handler.PARAMS[key]["value"] = write_handler.PARAMS[key]["handler"](args)

    for i in range(len(args)):
        args[i] = int(args[i], 16)

    try:
        status = ipBus.write(args[0], args[1:], write_handler.PARAMS["--FIFO"]["value"])
    except TimeoutError:
        return Error.TIMEOUT, "Timeout error"
    if status == Error.OK:
        return Error.OK, "Write successful"
    else:
        return Error.TRANSACTION, IPBus.TransactionInfoCodeStringType[status]


def RMWbits(*args, ipBus: IPBus.IPBus):
    args = list(args)

    for i in range(len(args)):
        args[i] = int(args[i], 16)

    data = ipBus.readModifyWriteBits(args[0], args[1], args[2])
    
    return readToString(args[0], [data], False)

def RMWsum(*sum, ipBus: IPBus.IPBus):
    args = list(sum)
    for i in range(len(args)):
        args[i] = int(args[i], 16)

    data = ipBus.readModifyWriteSum(args[0], args[1])
    return readToString(args[0], [data], False)



