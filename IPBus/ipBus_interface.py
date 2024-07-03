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
    address = ADDRESS("localhost", 50001)
    # address = ADDRESS("172.20.75.175", 50001)
    nextPackeID: int
    status = StatusPacket()

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        

    def __del__(self):
        self.socket.close()


    def _writingOK(self, toSend) -> bool:
        if not toSend is bytearray: toSend = bytearray(toSend)
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
        return self.status.packetHeader.packetType

    def read(self, startRegisterAddress: int, nWords: int, FIFO: bool) -> tuple[int, tuple[int, list[int]]]:
        '''
            Read from register:
                !!! Max read size: 255 words

            Returns
            -------
            int, bytearray
                int : 
                    0 if success,
                    -1 if client error,
                    other within TransactionInfoCodecStringType
                list[int]:
                    data[1] : list[int] : list of data read
        '''
        transactionType = TransactionType["read"] if not FIFO else TransactionType["nonIncrementingRead"]
        header = TransactionHeader(transactionType, nWords, id=0)
        toSend = header.toBytesArray("little")
        toSend = [*toSend, *startRegisterAddress.to_bytes(4, "little")]

        if not self._writingOK(toSend):
            return -1, None

        
        status, data = self._readingOK()
        if not status:
            return -1, None

        header.fromBytesArray(data[0:4])

        readWords = []
        for i in range(4, len(data), 4):
            readWords.append(int.from_bytes(data[i:i+4], "little"))
        
        return header.infoCode, readWords

    def write(self, startRegisterAddress: int, data: list[int], FIFO: bool):
        '''
            Write to register:
                !!! Max write size: 255 words

            Returns
            -------
            int
                0 if success,
                -1 if client error,
                other within TransactionInfoCodecStringType
        '''
        if not data is list: data = [data]


        transactionType = TransactionType["write"] if not FIFO else TransactionType["nonIncrementingWrite"]
        header = TransactionHeader(transactionType, len(data), id=0)
        toSend = header.toBytesArray()
        toSend = [*toSend, *startRegisterAddress.to_bytes(4, "little")]

        for word in data:
            toSend = [*toSend, *word.to_bytes(4, "little")]

        if not self._writingOK(toSend):
            return -1

        status, data = self._readingOK()
        if not status:
            return -1

        header.fromBytesArray(data[0:4])
        return header.infoCode


    def readModifyWriteBits(self, registerAddress: int, ANDmask: int, ORmask: int) -> int:
        header = TransactionHeader(TransactionType["RMWbits"], 1, id=0)
        toSend = header.toBytesArray()
        toSend = [*toSend, *registerAddress.to_bytes(4, "little")]
        toSend = [*toSend, *ANDmask.to_bytes(4, "little")]
        toSend = [*toSend, *ORmask.to_bytes(4, "little")]

        if not self._writingOK(toSend):
            return -1

        status, data = self._readingOK()
        if not status:
            return -1
        
        return int.from_bytes(data[0:4], "little")

    def readModifyWriteSum(self, registerAddress: int, addend: int) -> int:
        header = TransactionHeader(TransactionType["RMWsum"], 1, id=0)
        toSend = header.toBytesArray()
        toSend = [*toSend, *registerAddress.to_bytes(4, "little")]
        toSend = [*toSend, *addend.to_bytes(4, "little")]

        if not self._writingOK(toSend):
            return -1

        status, data = self._readingOK()
        if not status:
            return -1

        return int.from_bytes(data[0:4], "little")




if __name__ == '__main__':
    ipBus = IPBus()

    # ipBus.statusRequest()
    # ipBus.statusResponse()

    print(ipBus.read(0x10, 2, False))
    # print(ipBus.write(0x10, 0x16, False))

