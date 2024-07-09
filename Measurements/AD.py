import sys
from time import sleep
import dwfpy as dwf

VOLTAGE_RANGE = [25, 10, 2, 1, 500e-3, 200e-3, 100e-3, 50e-3, 20e-3, 10e-3, 5e-3, 2e-3, 1e-3, 0.5e-3, 0.2e-3]

def powerOn(device: dwf.Device):
    device.analog_io[0][0].value = True
    device.analog_io.master_enable = True

def rawMeasure(device: dwf.Device, channel: int = 0, rangeIndex: int = 0) -> float:
        scope = device.analog_input
        scope.channels[channel].setup(range=VOLTAGE_RANGE[rangeIndex])
        scope.configure()
        scope.read_status()
        data =  device.analog_input.channels[channel].get_sample()
        return data

def measure(device: dwf.Device, channel: int = 0, rangeIndex: int = -1) -> float:
        if rangeIndex != -1:
            data = rawMeasure(device, channel, rangeIndex)
            return data

        data = rawMeasure(device, channel, rangeIndex)
        for i in range(1, len(VOLTAGE_RANGE)-1):
            if abs(data) > VOLTAGE_RANGE[i]:
                rangeIndex = i-1
                # print(f"Range: {VOLTAGE_RANGE[rangeIndex]}")
                break
        if rangeIndex == -1:
            rangeIndex = len(VOLTAGE_RANGE)-1

        data = rawMeasure(device, channel, rangeIndex)
        return data


if __name__ == "__main__":
    args = sys.argv[1:]
    with dwf.Device(0) as device:
        # powerOn(device)
        # sleep(1)
        try:
            data = measure(device, channel=int(args[0]))
        except dwf.WaveformsError as e:
            print(e)
            sys.exit(1)
        except ValueError as e:
            print(e)
            sys.exit(1)
    print(data)
    sys.exit(0)