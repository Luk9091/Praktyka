import sys
import nidaqmx
import nidaqmx.constants as constants

from time import sleep


def measure(channel: int, min_val: float = 0, max_val: float = 5) -> float:
    data: int
    with nidaqmx.Task() as task:
        chan = task.ai_channels.add_ai_voltage_chan(f"Dev1/ai{channel}", min_val=min_val, max_val=max_val)
        chan.ai_term_cfg = constants.TerminalConfiguration.RSE
        data = task.read()
    return data


if __name__ == "__main__":
    args = sys.argv
    try:
        data = measure(args[1])
    except nidaqmx.DaqError as e:
        print(e)
        sys.exit(1)
    print(data)
    sys.exit(0)