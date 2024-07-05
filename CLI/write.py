def FIFO(args: list):
    args.remove("--FIFO")
    return True


PARAM = {
    "--FIFO": {"value": False, "handler": FIFO},
}