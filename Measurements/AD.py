import sys
import dwfpy as dwf

def measure(channel: int = 0) -> float:
    with dwf.AnalogDiscovery() as device:
        print(f"Found device: {device.name}")


if __name__ == "__main__":
    args = sys.argv
    # try:
    data = measure()
    # except dwf.Error as e:
    #     print(e)
    #     sys.exit(1)