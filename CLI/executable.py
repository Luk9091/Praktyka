import IPBus
import read as read_params
import write as write_params
from error_codes import Error

def interpretive_register(args: list, readWrite: str, register_map: dict = IPBus.registers.TCM_REGISTERS) -> tuple[Error, list[int], dict]:
    # REG = {"address": 0, "range": None, "readonly": False, "bits_pos": None, "additionalValue": IPBus.registers.TCM_REGISTERS}
    REG = {"address": 0, "range": None, "readonly": False, "bits_pos": None, "additionalValue": register_map}

    while REG["additionalValue"] is not None:
        try:
            register = REG["additionalValue"][args[0].upper()]
        except KeyError:
            return Error.INVALID_REGISTER, [], None
        args.pop(0)
        
        REG["address"] += register["address"]

        REG["additionalValue"] = register["additionalValue"]
        if register["range"] is not None:
            REG["range"] = register["range"]
        if register["readonly"] is not None:
            REG["readonly"] = register["readonly"]
        if register["bits_pos"] is not None:
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
        except (ValueError, IndexError):
            return Error.INVALID_VALUE, [], None


    return Error.INVALID_COMMAND, [], None


def convertStrToInt(value: str) -> int:
    if value.startswith("0x"):
        return int(value, 16)
    elif value.startswith("0b"):
        return int(value, 2)
    else:
        return int(value)

def args_to_int(args: list, readWrite: str, register_map: dict = IPBus.registers.TCM_REGISTERS) -> tuple[Error, list[int]]:
    try: 
        if args[0].upper() in register_map.keys():
            return interpretive_register(args, readWrite, register_map=register_map)
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

def set_ip(args: list, ipBus: IPBus.IPBus, register_dictionary: dict = None) -> tuple[Error, str]:
    if (args is None) or (len(args) == 0):
        return Error.OK, "Current IP: %s:%d" % (ipBus.address.IP, ipBus.address.port)
    
    ipBus.address.IP = args[0]
    if len(args) > 1:
        ipBus.address.port = args[1]
    
    return Error.OK, "IP address set to %s:%d" % (ipBus.address.IP, ipBus.address.port)

def read_status(args: list, ipBus: IPBus.IPBus, register_dictionary: dict = None) -> tuple[Error, str]:
    ipBus.statusRequest()
    try:
        status = ipBus.statusResponse()
    except TimeoutError:
        return Error.TIMEOUT, "Timeout error"
    
    if status == IPBus.PacketType["status"]:
        return Error.OK, "IPBus status OK"
    
    return Error.STATUS_REQUEST, "IPBus status request failed"


def convertIntToStr(value, base) -> str:
    if base == 16:
        return f"0x{value:08X}"
    elif base == 2:
        return f"0b{value:032b}"
    else:
        return str(value)

def readToString(startAddress: int, data: list[int], FIFO: bool, base: int) -> str:
    string = ""

    if not FIFO:
        if len(data) == 1:
            string = convertIntToStr(data[0], base)
        else:
            for i in range(len(data)):
                string += convertIntToStr(data[i], base)
                if i != len(data) - 1:
                    string += ", "
    else:
        # string =  "0x%08X:" % startAddress
        string = convertIntToStr(data[0], base)
        for i in range(1, len(data)):
            string += ", " + convertIntToStr(data[i], base)

    read_params.base = read_params.default_base
    return string.rstrip("\n")

def read(args: list, ipBus: IPBus.IPBus, register_dictionary: dict = IPBus.registers.TCM_REGISTERS) -> tuple[Error, str]:
    args = list(args)
    PARAMS = read_params.getParams()
    for key in PARAMS.keys():
        if key in args:
            PARAMS[key]["value"] = PARAMS[key]["handler"](args)

    error, args, reg = args_to_int(args, "read", register_map=register_dictionary)
    if error != Error.OK:
        return error, "Invalid arguments"


    try: 
        status, data = ipBus.read(args[0], PARAMS["-n"]["value"], PARAMS["--FIFO"]["value"], signed=PARAMS["-s"]["value"])
    except TimeoutError:
        return Error.TIMEOUT, "Timeout error"

    if (status != 0):
        return Error.TRANSACTION, IPBus.TransactionInfoCodeStringType[status]
    
    if reg is not None:
        data[0] = (data[0] & ((2**reg["bits_pos"]["LEN"]-1) << reg["bits_pos"]["LSB"])) >> reg["bits_pos"]["LSB"]
        if reg["range"]["min"] < 0:
            PARAMS["-s"]["value"] = True

    base = 10
    if PARAMS["-H"]["value"] == 16:
        base = 16
    elif PARAMS["-B"]["value"] == 2:
        base = 2
    return Error.OK, readToString(args[0], data, PARAMS["--FIFO"]["value"], base)


def write(args: list, ipBus: IPBus.IPBus, register_dictionary: dict = IPBus.registers.TCM_REGISTERS) -> tuple[Error, str]:
    args = list(args)
    PARAMS = write_params.getParams()

    for key in PARAMS.keys():
        if key in args:
            PARAMS[key]["value"] = PARAMS[key]["handler"](args)

    error, args, _ = args_to_int(args, "write", register_map=register_dictionary)
    if error != Error.OK:
        return error, "Invalid arguments"

    try:
        status = ipBus.write(args[0], args[1:], PARAMS["--FIFO"]["value"])
    except TimeoutError:
        return Error.TIMEOUT, "Timeout error"
    

    if status == Error.OK.value:
        return Error.OK, "Write successful"
    else:
        return Error.TRANSACTION, IPBus.TransactionInfoCodeStringType[status]


def RMWbits(args: list, ipBus: IPBus.IPBus, register_dictionary: dict = IPBus.registers.TCM_REGISTERS) -> tuple[Error, str]:
    args = list(args)
    base = read_params.default_base
    if "-H" in args:
        base = 16
        args.remove("-H")
    elif "-B" in args:
        base = 2
        args.remove("-B")

    error, args, reg = args_to_int(args, "read", register_map=register_dictionary)
    if error != Error.OK:
        return error, "Invalid arguments"

    try:
        infoCode, data = ipBus.readModifyWriteBits(args[0], args[1], args[2])
    except TimeoutError:
        return Error.TIMEOUT, "Timeout error"
    
    if infoCode != 0:
        return Error.TRANSACTION, IPBus.TransactionInfoCodeStringType[infoCode]
    return Error.OK, readToString(args[0], [data], False, base)

def RMWsum(args: list, ipBus: IPBus.IPBus, register_dictionary: dict = IPBus.registers.TCM_REGISTERS) -> tuple[Error, str]:
    args = list(args)
    base = read_params.default_base
    if "-H" in args:
        base = 16
        args.remove("-H")
    elif "-B" in args:
        base = 2
        args.remove("-B")

    error, args, reg = args_to_int(args, "read", register_map=register_dictionary)
    if error != Error.OK:
        return error, "Invalid arguments"
    
    signed = False
    if reg is not None:
        if reg["range"]["min"] < 0:
            signed = True
            
    try:
        status, data = ipBus.readModifyWriteSum(args[0], args[1], signed)
    except TimeoutError:
        return Error.TIMEOUT, "Timeout error"

    if status != 0:
        return Error.TRANSACTION, IPBus.TransactionInfoCodeStringType[status]
    return Error.OK, readToString(args[0], [data], False, base)



def set_bit(args: list, ipBus: IPBus.IPBus, register_dictionary: dict = IPBus.registers.TCM_REGISTERS) -> tuple[Error, str]:
    args = list(args)
    base = read_params.default_base
    if "-H" in args:
        base = 16
        args.remove("-H")
    elif "-B" in args:
        base = 2
        args.remove("-B")

    error, args, reg = args_to_int(args, "read", register_map=register_dictionary)
    # if reg is None:
    #     return Error.INVALID_REGISTER, "Enter register address by name"
    if error != Error.OK:
        return error, "Invalid arguments"
    
    
    try:
        ORmask = 2**args[1]
        bits = args[1]
    except IndexError:
        ORmask = 1
        bits = 0
        
    if reg is not None:
        if ORmask > reg["range"]["max"]:
            return Error.INVALID_VALUE, "Out of range, max bit: %d" % (reg["bits_pos"]["LEN"] - 1)
        ORmask  = ORmask << reg["bits_pos"]["LSB"]
    ANDmask = 0xFFFF_FFFF ^ ORmask
    
    try:
        status, data = ipBus.readModifyWriteBits(args[0], ANDmask, ORmask)
    except TimeoutError:
        return Error.TIMEOUT, "Timeout error"
    if status != 0:
        return Error.TRANSACTION, IPBus.TransactionInfoCodeStringType[status]
    
    data = (data >> bits) & 1
    return Error.OK, readToString(args[0], [data], False, base)

def clear_bit(args: list, ipBus: IPBus.IPBus, register_dictionary: dict = IPBus.registers.TCM_REGISTERS) -> tuple[Error, str]:
    args = list(args)
    base = read_params.default_base
    if "-H" in args:
        base = 16
        args.remove("-H")
    elif "-B" in args:
        base = 2
        args.remove("-B")

    error, args, reg = args_to_int(args, "read", register_map=register_dictionary)
    # if reg is None:
    #     return Error.INVALID_REGISTER, "Enter register address by name"
    if error != Error.OK:
        return error, "Invalid arguments"
    
    
    try:
        ORmask = 2**args[1]
        bits = args[1]
    except IndexError:
        ORmask = 1
        bits = 0
        
    if reg is not None:
        if ORmask > reg["range"]["max"]:
            return Error.INVALID_VALUE, "Out of range, max bit: %d" % (reg["bits_pos"]["LEN"] - 1)
        ORmask  = ORmask << reg["bits_pos"]["LSB"]
    ANDmask = 0xFFFF_FFFF ^ ORmask
    
    try:
        status, data = ipBus.readModifyWriteBits(args[0], ANDmask, 0)
    except TimeoutError:
        return Error.TIMEOUT, "Timeout error"
    if status != 0:
        return Error.TRANSACTION, IPBus.TransactionInfoCodeStringType[status]
    
    data = (data >> bits)
    return Error.OK, readToString(args[0], [data], False, base)





if __name__ == "__main__":
    print("This is not main module -- unit test of execute_command")
    data = "PMA0 OR_GATE 7"
    print(interpretive_register(data.split(" "), "read"))
    print(interpretive_register(data.split(" "), "write"))

    data = "temperature 2"
    print(interpretive_register(data.split(" "), "read"))
    print(interpretive_register(data.split(" "), "write"))

    data = "DONT_EXIST 2"
    print(interpretive_register(data.split(" "), "read"))
    print(interpretive_register(data.split(" "), "write"))