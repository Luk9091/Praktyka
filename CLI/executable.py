import IPBus
import read as read_handler
import write as write_handler
from error_codes import Error

def interpretive_register(args: list, readWrite: str) -> tuple[Error, list[int], dict]:
    REG = {"address": 0, "range": None, "readonly": False, "bits_pos": None, "additionalValue": IPBus.registers.TCM_REGISTERS}

    while not REG["additionalValue"] is None:
        try:
            register = REG["additionalValue"][args[0].upper()]
        except KeyError:
            return Error.INVALID_REGISTER, [], None
        args.pop(0)
        
        REG["address"] += register["address"]

        REG["additionalValue"] = register["additionalValue"]
        if not register["range"] is None:
            REG["range"] = register["range"]
        if not register["readonly"] is None:
            REG["readonly"] = register["readonly"]
        if not register["bits_pos"] is None:
            REG["bits_pos"] = register["bits_pos"]

    for i in range(len(args)):
        args[i] = convertStrToInt(args[i])

    if readWrite == "read":
        return Error.OK, [REG["address"], *args], REG


    if readWrite == "write":
        if REG["readonly"]:
            return Error.READ_ONLY, [], None

        try:
            value = int(args[0])
            if REG["range"]["min"] <= value <= REG["range"]["max"]:
                value = value << REG["bits_pos"]["LSB"]
                return Error.OK, [REG["address"], value], REG
            else:
                return Error.INVALID_VALUE, [], None
        except ValueError or IndexError:
            return Error.INVALID_VALUE, [], None


    return Error.INVALID_COMMAND, [], None


def convertStrToInt(value: str) -> int:
    if value.startswith("0x"):
        return int(value, 16)
    elif value.startswith("0b"):
        return int(value, 2)
    else:
        return int(value)

def args_to_int(args: list, readWrite: str) -> tuple[Error, list[int]]:
    try: 
        if args[0].upper() in IPBus.registers.TCM_REGISTERS.keys():
            return interpretive_register(args, readWrite)
    except IndexError:
        return Error.INVALID_VALUE, [], None


    for i in range(len(args)):
        args[i] = convertStrToInt(args[i])
    return Error.OK, args, None


def set_ip_as_param(args: list, ipBus: IPBus.IPBus):
    if (args is None) or (len(args) == 0):
        return Error.OK, "Current IP: %s:%d" % (ipBus.address.IP, ipBus.address.port)
        
    try:
        ipBus.address.IP = args.pop(args.index("--ip") + 1)
    except IndexError:
        return Error.INVALID_VALUE, "Cannot set new ip address"
        
    try:
        if args[args.index("--ip") + 1].isdigit():
            ipBus.address.port = int(args.pop(args.index("--ip") + 1))
    except IndexError:
        pass
        

    args.remove("--ip")

    return Error.OK, "IP address set to %s:%d" % (ipBus.address.IP, ipBus.address.port)

def set_ip(args: list, ipBus: IPBus.IPBus):
    if (args is None) or (len(args) == 0):
        return Error.OK, "Current IP: %s:%d" % (ipBus.address.IP, ipBus.address.port)
    
    ipBus.address.IP = args[0]
    if len(args) > 1:
        ipBus.address.port = args[1]
    
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


def convertIntToStr(value, base):
    if base == 16:
        return f"0x{value:08X}"
    elif base == 2:
        return f"0b{value:032b}"
    else:
        return str(value)

def readToString(startAddress: int, data: list[int], FIFO: bool, base: int) -> str:
    string = ""

    if not FIFO:
        for i in range(len(data)):
            string = convertIntToStr(data[i], base)
    else:
        # string =  "0x%08X:" % startAddress
        string = convertIntToStr(data[0], base)
        for i in range(1, len(data)):
            string += ", " + convertIntToStr(data[i], base)

    read_handler.base = read_handler.default_base
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


def write(args: list, ipBus: IPBus.IPBus) -> tuple[Error, str]:
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


def RMWbits(args: list, ipBus: IPBus.IPBus) -> tuple[Error, str]:
    args = list(args)
    base = read_handler.default_base
    for i in range(len(args)):
        if args[i] == "-H":
            base = 16
            args.pop(i)
        elif args[i] == "-B":
            base = 2
            args.pop(i)

    error, args, _ = args_to_int(args, "read")
    if error != Error.OK:
        return error, "Invalid arguments"

    data = ipBus.readModifyWriteBits(args[0], args[1], args[2])
    
    return Error.OK, readToString(args[0], [data], False, base)

def RMWsum(args: list, ipBus: IPBus.IPBus) -> tuple[Error, str]:
    args = list(args)
    base = read_handler.default_base
    for i in range(len(args)):
        if args[i] == "-H":
            base = 16
            args.remove("-H")
        elif args[i] == "-B":
            base = 2
            args.remove("-B")

    error, args, _ = args_to_int(args, "read")
    if error != Error.OK:
        return error, "Invalid arguments"
    
    data = ipBus.readModifyWriteSum(args[0], args[1])
    return Error.OK, readToString(args[0], [data], False, base)




if __name__ == "__main__":
    print("This is not main module -- unit test of execute_command")
    data = "PM0 OR_GATE 7"
    data = data.split(" ")
    print(interpretive_register(data, "read"))
    print(interpretive_register(data, "write"))

    data = "temperature 2"
    data = data.split(" ")
    print(interpretive_register(data, "read"))
    print(interpretive_register(data, "write"))

    data = "temperature 2"
    data = data.split(" ")
    print(interpretive_register(data, "read"))
    print(interpretive_register(data, "write"))