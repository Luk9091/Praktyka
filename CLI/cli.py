import sys
from socket import timeout as TimeoutError
from enum import Enum
from pathlib import Path

import IPBus
from error_codes import Error
from executable import *
ipBus = IPBus.IPBus()


outputFile = None
csvFormat = False

class State(Enum):
    CLI = 1
    READ_FILE = 2
    OK_EXIT = 3
    ERR_EXIT = 4
    ERROR = 100

def OK_exit(args: list, ipBus=None) -> None:
    # print()
    # print("Exiting...")
    exit(0)
def ERR_exit(args: list, ipBus=None) -> None:
    exit(1)

def CSV_format(args: list, ipBus=None):
    csvFormat = True

def help(args, ipBus = None):
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

def execute_command(args: list) -> tuple[Error, str]:
    args = list(args)
    if len(args) == 0:
        ans = "Missing command. \nValid: %s" % ", ".join(COMMANDS.keys())
        return Error.INVALID_COMMAND, ans

    cmd = args[0].lower()
    args = args[1:]

    try:
        if len(args) < COMMANDS[cmd]["minargs"]:
            ans = "Missing arguments.\nUsage: %s" % COMMANDS[cmd]["usage"]
            return Error.INVALID_COMMAND, ans
    except KeyError:
        ans = "Invalid command. \nValid: %s" % ", ".join(COMMANDS.keys())
        return Error.INVALID_COMMAND, ans

    if "--help" in args:
        status, ans = help(cmd)
        return status, ans
    
    try:
        error, ans = COMMANDS[cmd]["handler"](args, ipBus=ipBus)
    except ValueError:
        return Error.INVALID_COMMAND, "Invalid arguments"

    return error, ans

def Init(args: list) -> State:
    state = State.CLI

    for cmd in args:
        if cmd in PARAMS.keys():
            PARAMS[cmd]["handler"](args, ipBus=ipBus)
            if PARAMS[cmd]["nextState"].value > state.value:
                state = PARAMS[cmd]["nextState"]
            continue

    for cmd in args:
        if cmd in COMMANDS.keys():
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
    try:
        while True:
            read = input(f"{ipBus.address.IP} << ")
            read = read.split(" ")
            
            status, ans = execute_command(read)
            if status == Error.OK:
                print(ans)
            else:
                print(f"Error: {ans}")
    except KeyboardInterrupt:
        OK_exit()
        

def write_file():
    pass

def read_file(args: list):
    pass

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
    "read"   : {"minargs": 1, "handler": read,          "usage": "read [address | name] ([-n] [value]) ([--FIFO])"},
    "write"  : {"minargs": 2, "handler": write,         "usage": "write [address | name] [value] ([values]...) ([--FIFO])"},
    "rmwbits": {"minargs": 3, "handler": RMWbits,       "usage": "RMWbits [address | name] [mask] [value]"},
    "rmwsum" : {"minargs": 1, "handler": RMWsum,        "usage": "RMWsum [address | name] [value]"},
    "help"   : {"minargs": 0, "handler": help,          "usage": "help ([command])"},
    "exit"   : {"minargs": 0, "handler": OK_exit,       "usage": "Just exit"},
}

PARAMS = {
    "-i"    : {"minargs": 2, "handler": None,       "nextState": State.READ_FILE,   "usage": "[file] -- read from file | default: stdin"},
    "-o"    : {"minargs": 2, "handler": None,       "nextState": State.CLI,         "usage": "[file] -- store output to file | default: only display on stdout"},
    "--ip"  : {"minargs": 2, "handler": set_ip,     "nextState": State.CLI,         "usage": "[ip] ([port])"},
    "--csv" : {"minargs": 0, "handler": CSV_format, "nextState": State.CLI,         "usage": "output in csv format"},
    "--help": {"minargs": 0, "handler": param_help, "nextState": State.OK_EXIT,     "usage": "display help"},
}



if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
