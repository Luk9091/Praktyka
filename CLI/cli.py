import sys
import IPBus
from socket import timeout as TimeoutError
import read as read_handler
import write as write_handler

ipBus = IPBus.IPBus()

def set_ip(*args):
    if (args is None) or (len(args) == 0):
        return "Current IP: %s:%d" % (ipBus.address.IP, ipBus.address.port)
        
    ipBus.address.IP = args[0]

    if len(args) > 1:
        ipBus.address.port = int(args[1])

    return "IP address set to %s:%d" % (ipBus.address.IP, ipBus.address.port)

def read_status(*args):
    ipBus.statusRequest()
    if ipBus.statusResponse() == IPBus.PacketType["status"]:
        return "IPBus status OK"
    
    return ""

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

def read(*args):
    args = list(args)
    for key in read_handler.PARAMS.keys():
        if key in args:
            read_handler.PARAMS[key]["value"] = read_handler.PARAMS[key]["handler"](args)

    for i in range(len(args)):
        args[i] = int(args[i], 16)



    status, data = ipBus.read(args[0], read_handler.PARAMS["-n"]["value"], read_handler.PARAMS["--FIFO"]["value"])

    if (status != 0):
        return IPBus.TransactionInfoCodeStringType[status]
    
    return readToString(args[0], data, read_handler.PARAMS["--FIFO"]["value"])


def write(*args):
    args = list(args)

    for key in read_handler.PARAMS.keys():
        if key in args:
            write_handler.PARAM[key]["value"] = write_handler.PARAM[key]["handler"](args)

    for i in range(len(args)):
        args[i] = int(args[i], 16)

    return ipBus.write(args[0], args[1:], write_handler.PARAMS["--FIFO"]["value"])

def RMWbits(*args):
    args = list(args)

    for i in range(len(args)):
        args[i] = int(args[i], 16)

    data = ipBus.readModifyWriteBits(args[0], args[1], args[2])
    return readToString(args[0], [data], False)

def RMWsum(*sum):
    args = list(sum)
    for i in range(len(args)):
        args[i] = int(args[i], 16)

    data = ipBus.readModifyWriteSum(args[0], args[1])
    return readToString(args[0], [data], False)



COMMANDS = {
    "ip"     : {"minargs": 0, "handler": set_ip},
    "status" : {"minargs": 0, "handler": read_status},
    "read"   : {"minargs": 1, "handler": read},
    "write"  : {"minargs": 2, "handler": write},
    "rmwbits": {"minargs": 3, "handler": RMWbits},
    "rmwsum" : {"minargs": 1, "handler": RMWsum},
}



if __name__ == "__main__":
    args = sys.argv[1:]
    print(args, len(args))

    if len(args) == 0:
        print("Missing command. Valid: %s" % ", ".join(COMMANDS.keys()))
        sys.exit(-1)

    cmd = args[0].lower()
    args = args[1:]

    if len(args) < COMMANDS[cmd]["minargs"]:
        print("Missing arguments. Usage: %s" % cmd)
        sys.exit(-1)
    
    try:
        print(COMMANDS[cmd]["handler"](*args))
    except TimeoutError:
        print("Timeout error")