import IPBus
import read as read_handler
import write as write_handler
from error_codes import Error

def interpretive_register(args: list) -> tuple[Error, list[int]]:
    i = 0
    try:
        register = IPBus.registers.TCM_REGISTERS[args[i]]
    except KeyError:
        return Error.INVALID_COMMAND, []

    address = register["address"]
    if register["range"] is not None:
        Range = register["range"]
    while register["additionalValue"] is not None:
        i += 1

        try:
            register = register["additionalValue"][args[i]]
        except KeyError:
            return Error.INVALID_COMMAND, []

        if register["range"] is not None:
            Range = register["range"]
        address += register["address"]

    try:
        value = int(args[i+1])
        if Range["min"] <= value <= Range["max"]:
            return Error.OK, [address, value]
    except ValueError:
        return Error.INVALID_COMMAND, []


    return Error.INVALID_COMMAND, []

def args_to_int(args: list) -> list[int]:
    for i in range(len(args)):
        if args[i].startswith("0x"):
            args[i] = int(args[i][2:], 16)
        elif args[i].startswith("0b"):
            args[i] = int(args[i][2:], 2)
        else:
            args[i] = int(args[i])
    return args


def set_ip(args: list, ipBus: IPBus.IPBus):
    if (args is None) or (len(args) == 0):
        return Error.OK, "Current IP: %s:%d" % (ipBus.address.IP, ipBus.address.port)
        
    # ipBus.address.IP = args[0]
    ipBus.address.IP = args.pop(args.index("--ip") + 1)
    args.remove("--ip")

    # if len(args) > 1:
    #     try:
    #         ipBus.address.port = int(args[1])
    #     except ValueError:
    #         return Error.INVALID_COMMAND, "Port must be an integer."

    return Error.OK, "IP address set to %s:%d" % (ipBus.address.IP, ipBus.address.port)

def read_status(args: list, ipBus: IPBus.IPBus):
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
            # string += "0x%08X: " % (startAddress + i)
            # string += "0x%08X\n" % (data[i])
            string += f"{data[i]}\n"
    else:
        string =  "0x%08X:" % startAddress
        for i in range(len(data)):
            string += " 0x%08X" % data[i]

    return string.rstrip("\n")

def read(args: list, ipBus: IPBus.IPBus):
    args = list(args)
    for key in read_handler.PARAMS.keys():
        if key in args:
            read_handler.PARAMS[key]["value"] = read_handler.PARAMS[key]["handler"](args)
            # args.remove(key)

    args = args_to_int(args)
    # for i, value in enumerate(args):
    #     # try:
    #     args[i] = int(args[i])
    #     # except ValueError:
    #     #     args[i] = interpretive_register(args, i)


    try: 
        status, data = ipBus.read(args[0], read_handler.PARAMS["-n"]["value"], read_handler.PARAMS["--FIFO"]["value"], signed=read_handler.PARAMS["-s"]["value"])
    except TimeoutError:
        return Error.TIMEOUT, "Timeout error"

    if (status != 0):
        return Error.TRANSACTION, IPBus.TransactionInfoCodeStringType[status]
    
    return Error.OK, readToString(args[0], data, read_handler.PARAMS["--FIFO"]["value"])


def write(args: list, ipBus: IPBus.IPBus):
    args = list(args)

    for key in read_handler.PARAMS.keys():
        if key in args:
            write_handler.PARAMS[key]["value"] = write_handler.PARAMS[key]["handler"](args)

    # for i in range(len(args)):
    #     args[i] = int(args[i])
    args = args_to_int(args)

    try:
        status = ipBus.write(args[0], args[1:], write_handler.PARAMS["--FIFO"]["value"])
    except TimeoutError:
        return Error.TIMEOUT, "Timeout error"
    if status == Error.OK.value:
        return Error.OK, "Write successful"
    else:
        return Error.TRANSACTION, IPBus.TransactionInfoCodeStringType[status]


def RMWbits(args: list, ipBus: IPBus.IPBus):
    args = list(args)

    args = args_to_int(args)

    data = ipBus.readModifyWriteBits(args[0], args[1], args[2])
    
    return readToString(args[0], [data], False)

def RMWsum(args: list, ipBus: IPBus.IPBus):
    for i in range(len(args)):
        args[i] = int(args[i])

    data = ipBus.readModifyWriteSum(args[0], args[1])
    return readToString(args[0], [data], False)




if __name__ == "__main__":
    data = "PM0 OR_GATE 7"
    data = data.split(" ")
    print(interpretive_register(data))

    data = "RESET_COUNTER 2"
    data = data.split(" ")
    print(interpretive_register(data))
