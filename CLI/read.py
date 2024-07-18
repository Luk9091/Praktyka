default_base = 10

def FIFO(args: list):
    args.remove("--FIFO")
    return True
    
def SIGNED(args: list):
    args.remove("-s")
    return True

def nWords(args: list):
    value = 1
    try:
        value = int(args.pop(args.index("-n") + 1))
    except ValueError:
        pass
    args.remove("-n")
    return value


def toHex(args: list):
    args.remove("-H")
    return 16

def toBin(args: list):
    args.remove("-B")
    return 2

def getParams():
    PARAMS = {
        "-H"    : {"value": 10,    "handler": toHex},
        "-B"    : {"value": 10,    "handler": toBin},
        "--FIFO": {"value": False, "handler": FIFO},
        "-n"    : {"value": 1,     "handler": nWords},
        "-s"    : {"value": False, "handler": SIGNED},
    }

    return PARAMS