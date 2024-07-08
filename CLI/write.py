def FIFO(args: list):
    args.remove("--FIFO")
    return True


PARAMS = {
    "--FIFO": {"value": False, "handler": FIFO},
}