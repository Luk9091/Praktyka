import IPBus
import read as read_handler
import write as write_handler
from error_codes import Error

def interpretive_register(args: list, readWrite: str) -> tuple[Error, list[int], dict]:
    i = 0
    REG = {"address": 0, "range": None, "readonly": False, "bits_pos": None, "additionalValue": IPBus.registers.TCM_REGISTERS}

    while not REG["additionalValue"] is None:
        try:
            register = REG["additionalValue"][args[i].upper()]
        except KeyError:
            return Error.INVALID_REGISTER, [], None
        
        REG["address"] += register["address"]

        REG["additionalValue"] = register["additionalValue"]
        if not register["range"] is None:
            REG["range"] = register["range"]
        if not register["readonly"] is None:
            REG["readonly"] = register["readonly"]
        if not register["bits_pos"] is None:
            REG["bits_pos"] = register["bits_pos"]

        i += 1

    if readWrite == "read":
        return Error.OK, [REG["address"]], REG


    if readWrite == "write":
        if REG["readonly"]:
            return Error.READ_ONLY, [], None

        try:
            value = int(args[i+1])
            if REG["range"]["min"] <= value <= REG["range"]["max"]:
                value = value << REG["bits_pos"]["LSB"]
                return Error.OK, [REG["address"], value], REG
            else:
                return Error.INVALID_VALUE, [], None
        except ValueError or IndexError:
            return Error.INVALID_VALUE, [], None


    return Error.INVALID_COMMAND, [], None

def args_to_int(args: list, readWrite: str) -> tuple[Error, list[int]]:

    if args[0].upper() in IPBus.registers.TCM_REGISTERS.keys():
        return interpretive_register(args, readWrite)


    for i in range(len(args)):
        if args[i].startswith("0x"):
            args[i] = int(args[i][2:], 16)
        elif args[i].startswith("0b"):
            args[i] = int(args[i][2:], 2)
        else:
            args[i] = int(args[i])
    return Error.OK, args, None


def set_ip(args: list, ipBus: IPBus.IPBus):
    if (args is None) or (len(args) == 0):
        return Error.OK, "Current IP: %s:%d" % (ipBus.address.IP, ipBus.address.port)
        
    ipBus.address.IP = args.pop(args.index("--ip") + 1)
    args.remove("--ip")

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

def readToString(startAddress: int, data: list[int], FIFO: bool, base: int) -> str:
    string = ""

    if not FIFO:
        for i in range(len(data)):
            if (base == 16):
                string += f"0x{data[i]:08X}\n"
            elif (base == 2):
                string += f"0b{data[i]:032b}\n"
            else:
                string += f"{data[i]}\n"
    else:
        string =  "0x%08X:" % startAddress
        for i in range(len(data)):
            string += " 0x%08X" % data[i]

    return string.rstrip("\n")

def read(args: list, ipBus: IPBus.IPBus) -> tuple[Error, str]:
    args = list(args)
    for key in read_handler.PARAMS.keys():
        if key in args:
            read_handler.PARAMS[key]["value"] = read_handler.PARAMS[key]["handler"](args)
            # args.remove(key)

    error, args, reg = args_to_int(args, "read")
    if error != Error.OK:
        return error, "Invalid arguments"


    try: 
        status, data = ipBus.read(args[0], read_handler.PARAMS["-n"]["value"], read_handler.PARAMS["--FIFO"]["value"], signed=read_handler.PARAMS["-s"]["value"])
    except TimeoutError:
        return Error.TIMEOUT, "Timeout error"

    if (status != 0):
        return Error.TRANSACTION, IPBus.TransactionInfoCodeStringType[status]
    
    ans = data[0]
    if not reg is None:
        ans = (ans & ((2**reg["bits_pos"]["LEN"]-1) << reg["bits_pos"]["LSB"])) >> reg["bits_pos"]["LSB"]
        if reg["range"]["min"] < 0:
            read_handler.PARAMS["-s"]["value"] = True

    return Error.OK, readToString(args[0], data, read_handler.PARAMS["--FIFO"]["value"], read_handler.base)


def write(args: list, ipBus: IPBus.IPBus):
    args = list(args)

    for key in read_handler.PARAMS.keys():
        if key in args:
            write_handler.PARAMS[key]["value"] = write_handler.PARAMS[key]["handler"](args)

    # for i in range(len(args)):
    #     args[i] = int(args[i])
    error, args, _ = args_to_int(args, "write")
    if error != Error.OK:
        return error, "Invalid arguments"

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
    # data = "PM0 OR_GATE 7"
    # data = data.split(" ")
    # print(interpretive_register(data, "read"))
    # print(interpretive_register(data, "write"))

    # data = "temperature 2"
    # data = data.split(" ")
    # print(interpretive_register(data, "read"))
    # print(interpretive_register(data, "write"))

    data = "temperature 2"
    data = data.split(" ")
    print(interpretive_register(data, "read"))
    print(interpretive_register(data, "write"))