def FIFO(args: list):
    args.remove("--FIFO")
    return True


def getParams():
    PARAMS = {
        "--FIFO": {"value": False, "handler": FIFO},
    }
    return PARAMS