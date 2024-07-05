def FIFO(args: list):
    args.remove("--FIFO")
    return True

def nWords(args: list):
    value = 1
    try:
        value = int(args.pop(args.index("-n") + 1))
    except ValueError:
        pass
    args.remove("-n")
    return value


PARAMS = {
    "--FIFO": {"value": False, "handler": FIFO},
    "-n"    : {"value": 1,     "handler": nWords},
}