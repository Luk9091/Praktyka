import socket
from dataclasses import dataclass

from ipBus_header import *


@dataclass
class ADDRESS:
    address: str
    port: int

    def __call__(self) -> tuple:
        return (self.address, self.port)

class IPBus:
    # UDP_ADDRESS = ["localhost", 50001]
    address = ADDRESS("localhost", 50001)
    nextPackeID: int
    status = StatusPacket()

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        

    def __del__(self):
        self.socket.close()


    def _writingOK(self, toSend) -> bool:
        n: int = self.socket.sendto(toSend, self.address())
        if (n == -1):
            print(f"Socket write error")
            return False
        if (n != len(toSend)):
            print(f"Sending packed failed")
            return False
        return True

    def _readingOK(self) -> tuple[bool, bytearray]:
        data: bytes = self.socket.recvfrom(maxWordsPerPacket)
        readAddress = ADDRESS(data[1][0], data[1][1])
        data = data[0]
        
        if len(data) == 0:
            print(f"Empty data")
            return False, None
        return True, data

    def readRegisters(self, data: list[int], nWords: int, baseAddress: int, FIFO: bool) -> int:
        if nWords == 0: return -1

        extend  =2
        if nWords > 255: extend = 3
        if nWords + extend > maxWordsPerPacket: return -1

        # self.readRequest(data, nWords, baseAddress, FIFO)

    # def readRequest(self, data: list[int], nWords: int, baseAddress: int, FIFO: bool) -> int:

    def statusRequest(self) -> int:
        statusPacket = StatusPacket()
        if not self._writingOK(statusPacket.toBytesArray()):
            return -1
        return 0

    def statusResponse(self) -> int:
        status, data = self._readingOK()
        if not status:
            return -1

        self.status.fromBytesArray(data)
        return 0





if __name__ == '__main__':
    ipBus = IPBus()

    ipBus.statusRequest()
    ipBus.statusResponse()

