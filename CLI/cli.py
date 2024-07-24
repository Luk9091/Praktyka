import sys
from socket import timeout as TimeoutError
from enum import Enum
from pathlib import Path

import IPBus
from error_codes import Error
from executable import *
ipBus = IPBus.IPBus()


input_file: Path = None
output_file: Path = None

class State(Enum):
    CLI = 1
    READ_FILE = 2
    OK_EXIT = 3
    ERR_EXIT = 4
    ERROR = 100

def OK_exit(args: list = None, ipBus=None, register_dictionary = None) -> None:
    exit(0)
def ERR_exit(args: list = None, ipBus=None, register_dictionary = None) -> None:
    exit(1)

def set_inFile(args: list, ipBus=None):
    global input_file
    input_file = Path(args[args.index("-i") + 1])
    return Error.OK, "Input file set to %s" % input_file

def set_outFile(args: list, ipBus=None):
    global output_file
    output_file = Path(args[args.index("-o") + 1])
    return Error.OK, "Output file set to %s" % output_file

def help(args: list, ipBus = None, register_dictionary = None):
    if not isinstance(args, list):
        args = [args]
    if len(args) == 0:
        return Error.OK, "Available commands: %s" % ", ".join(COMMANDS.keys())

    try:
        status, ans = Error.OK, COMMANDS[args[0]]["usage"]
        ans = f" >> {ans}"
    except KeyError:
        status, ans = Error.INVALID_COMMAND, "Command not found"
    return status, ans

def param_help(args, ipBus = None):
    print("Available parameters: %s" % ", ".join(PARAMS.keys()))
    for key in PARAMS.keys():
        print(f"\t{key}: {PARAMS[key]['usage']}")
    return Error.OK, ""

def execute_command(args: list, register_dictionary: dict = IPBus.registers.TCM_REGISTERS) -> tuple[Error, str]:
    args = list(args)
    if "" in args:
        args.remove("")
    if len(args) == 0:
        # ans = "Missing command. \nValid: %s" % ", ".join(COMMANDS.keys())
        return Error.EMPTY_LINE, ""

    cmd = args[0].lower()
    args = args[1:]

    try:
        if len(args) < COMMANDS[cmd]["minargs"]:
            ans = "Missing arguments.\nUsage: %s" % COMMANDS[cmd]["usage"]
            return Error.INVALID_COMMAND, ans
    except KeyError:
        ans = "\tInvalid command. \n\tValid: %s" % ", ".join(COMMANDS.keys())
        return Error.INVALID_COMMAND, ans

    if "--help" in args:
        status, ans = help(cmd)
        return status, ans
    
    try:
        error, ans = COMMANDS[cmd]["handler"](args, ipBus=ipBus, register_dictionary=register_dictionary)
    except ValueError:
        return Error.INVALID_COMMAND, "Invalid arguments"

    if ipBus.transaction.infoCode != 0:
        return Error.TRANSACTION, ipBus.transaction.infoCodeString()
    return error, ans

def Init(args: list) -> State:
    state = State.CLI

    for key in PARAMS.keys():
        if key in args:
            error, msg = PARAMS[key]["handler"](args, ipBus=ipBus)
            if error != Error.OK:
                print(f"Error: {msg}")
                return State.ERR_EXIT

            if PARAMS[key]["nextState"].value > state.value:
                state = PARAMS[key]["nextState"]
                
            

    for key in COMMANDS.keys():
        if key in args:
            try:
                status, ans = execute_command(args)
                if status == Error.OK:
                    print(ans)
                else:
                    print(f"Error: {ans}")
            except TimeoutError:
                print("Timeout error")
                return State.ERR_EXIT
            finally:
                if status == Error.OK:
                    return State.OK_EXIT
                else:
                    return State.ERR_EXIT

    return state

        
def CLI(args: list):
    while True:
        try:
            read = input(f"{ipBus.address.IP} << ")
        except (KeyboardInterrupt, EOFError):
            OK_exit()

        if '#' in read:
            read = read[:read.index('#')]
        read = read.strip("\t")
        status, ans = execute_command(read.split(" "))
        if status == Error.OK:
            print(ans)
            if output_file is not None:
                write_file(ipBus.address.IP, read, ans)
        elif status == Error.EMPTY_LINE:
            continue
        else:
            ans = f"Error: {ans}"
            # if output_file is not None:
            #     write_file(ipBus.address.IP, read, ans)
            print(ans)
        # print(ipBus.header)
        # print(ipBus.transaction)
    

def write_file(dev, command, ans):
    with open(output_file, "a") as file:
       file.write(f"{dev}, {command}, {ans}\n")

def read_file(args: list):
    file = open(input_file, "r")
    for line in file:
        if '#' in line:
            line = line[:line.index('#')]

        line = line.strip("\t")
        line = line.strip("\n")
        line = line.strip("\r")

        status, ans = execute_command(line.split(" "))

        if status == Error.OK:
            print(ans)
            if output_file is not None:
                write_file(ipBus.address.IP, line, ans)
        elif status == Error.EMPTY_LINE:
            continue
        else:
            ans = f"Error: {ans}"
            if output_file is not None:
                write_file(ipBus.address.IP, line, ans)
            print(ans)
            break
    file.close()


def main(args: list):
    status = Init(args)
    STATE[status]["handler"](STATE[status]["args"])


STATE = {
    State.ERROR     : {"handler": ERR_exit,     "args": None},
    State.CLI       : {"handler": CLI,          "args": None},
    State.READ_FILE : {"handler": read_file,    "args": None},
    State.OK_EXIT   : {"handler": OK_exit,      "args": None},
    State.ERR_EXIT  : {"handler": ERR_exit,     "args": None},
}


COMMANDS = {
    "ip"     : {"minargs": 0, "handler": set_ip,        "usage": "ip [ip] ([port])"},
    "status" : {"minargs": 0, "handler": read_status,   "usage": "status ([--timeout] [value])"},
    "read"   : {"minargs": 1, "handler": read,          "usage": "read [address | name] ([-n] [value]) ([--FIFO]) ([-s]) ([-H/B])"},
    "write"  : {"minargs": 2, "handler": write,         "usage": "write [address | name] [value] ([values]...) ([--FIFO])"},
    "rmwbits": {"minargs": 3, "handler": RMWbits,       "usage": "RMWbits [address | name] [ANDmask] [ORmask] ([-H/-B])"},
    "rmwsum" : {"minargs": 1, "handler": RMWsum,        "usage": "RMWsum [address | name] [value] ([-H/-B]) ([-s])"},
    "setbit" : {"minargs": 1, "handler": set_bit,       "usage": "setBit [name] [bit | default = 0] ([-H/-B])"},
    "clearbit":{"minargs": 1, "handler": clear_bit,     "usage": "clearBit [name] [bit | default = 0] ([-H/-B])"},
    "help"   : {"minargs": 0, "handler": help,          "usage": "help ([command]) -- add command to get help"},
    "exit"   : {"minargs": 0, "handler": OK_exit,       "usage": "Just exit"},
}

PARAMS = {
    "-i"    : {"minargs": 2, "handler": set_inFile, "nextState": State.READ_FILE,   "usage": "[file] -- read from file | default: stdin"},
    "-o"    : {"minargs": 2, "handler": set_outFile,"nextState": State.CLI,         "usage": "[file] -- store output to file | default: only display on stdout"},
    "--ip"  : {"minargs": 2, "handler": set_ip_as_param, "nextState": State.CLI,    "usage": "[ip] ([port])"},
    "--help": {"minargs": 0, "handler": param_help, "nextState": State.OK_EXIT,     "usage": "([command]) -- display help"},
}



if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
