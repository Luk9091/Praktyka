import socket
from dataclasses import dataclass

if __name__ == '__main__':
    from ipBus_header import *
else:
    from .ipBus_header import *


@dataclass
class ADDRESS:
    IP: str
    port: int

    def __call__(self) -> tuple:
        return (self.IP, self.port)

class IPBus:
    address = ADDRESS("localhost", 50001)
    nextPackeID: int
    status = StatusPacket()

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(1)

    def __del__(self):
        self.socket.close()


    def __writing(self, toSend) -> bool:
        if not isinstance(toSend, bytearray): toSend = bytearray(toSend)
        n: int = self.socket.sendto(toSend, self.address())
        if (n == -1) or (n != len(toSend)):
            return False
        return True

    def __reading(self) -> tuple[bool, bytearray]:
        data: bytes = self.socket.recvfrom(maxWordsPerPacket)
        # readAddress = ADDRESS(data[1][0], data[1][1])
        data = data[0]
        
        if len(data) == 0:
            return False, None
        return True, data

    def statusRequest(self) -> int:
        statusPacket = StatusPacket()
        packetHeader = PacketHeader(PacketType["status"])
        toSend = statusPacket.toBytesArray()
        if not self.__writing(bytearray(toSend)):
            return -1
        return 0

    def statusResponse(self) -> int:
        status, data = self.__reading()
        if not status:
            return -1
        
        self.status.fromBytesArray(data)
        return self.status.packetHeader.packetType

    def read(self, startRegisterAddress: int, nWords: int, FIFO: bool, signed: bool = False) -> tuple[int, list[int]]:
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
        packetHeader = PacketHeader(PacketType["control"])
        toSend = packetHeader.toBytesArray("little")
        toSend = [*toSend, *header.toBytesArray("little")]
        toSend = [*toSend, *startRegisterAddress.to_bytes(4, "little")]

        if not self.__writing(toSend):
            return -1, None

        
        status, data = self.__reading()
        if not status:
            return -1, None

        header.fromBytesArray(data[0:4])

        readWords = []
        for i in range(8, len(data), 4):
            readWords.append(int.from_bytes(data[i:i+4], "little", signed=signed))
        
        return header.infoCode, readWords

    def write(self, startRegisterAddress: int, data: list[int], FIFO: bool, signed: bool = False) -> int:
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
        if not isinstance(data, list): data = [data]


        packetHeader = PacketHeader(PacketType["control"])
        transactionType = TransactionType["write"] if not FIFO else TransactionType["nonIncrementingWrite"]
        header = TransactionHeader(transactionType, len(data), id=0)
        toSend = packetHeader.toBytesArray("little")
        toSend = [*toSend, *header.toBytesArray()]
        toSend = [*toSend, *startRegisterAddress.to_bytes(4, "little")]

        for word in data:
            if (word < 0): signed = True
            else: signed = False
            toSend = [*toSend, *word.to_bytes(4, "little", signed=signed)]

        if not self.__writing(toSend):
            return -1

        status, data = self.__reading()
        if not status:
            return -1

        header.fromBytesArray(data[0:4])
        return header.infoCode


    def readModifyWriteBits(self, registerAddress: int, ANDmask: int, ORmask: int) -> int:
        header = TransactionHeader(TransactionType["RMWbits"], 1, id=0)
        packetHeader = PacketHeader(PacketType["control"])
        toSend = packetHeader.toBytesArray("little")
        toSend = [*toSend, *header.toBytesArray()]
        toSend = [*toSend, *registerAddress.to_bytes(4, "little")]
        toSend = [*toSend, *ANDmask.to_bytes(4, "little")]
        toSend = [*toSend, *ORmask.to_bytes(4, "little")]

        if not self.__writing(toSend):
            return -1

        status, data = self.__reading()
        if not status:
            return -1
        
        return int.from_bytes(data[8:12], "little")

    def readModifyWriteSum(self, registerAddress: int, addend: int, signed_read: bool = False) -> int:
        signed_add = False
        if addend < 0:
            signed_add = True

        header = TransactionHeader(TransactionType["RMWsum"], 1, id=0)
        packetHeader = PacketHeader(PacketType["control"])
        toSend = packetHeader.toBytesArray("little")
        toSend = [*toSend, *header.toBytesArray()]
        toSend = [*toSend, *registerAddress.to_bytes(4, "little")]
        toSend = [*toSend, *addend.to_bytes(4, "little", signed=signed_add)]

        if not self.__writing(toSend):
            return -1

        status, data = self.__reading()
        if not status:
            return -1

        return int.from_bytes(data[8:12], "little", signed=signed_read)




if __name__ == '__main__':
    from colorama import init as colorama_init
    from colorama import Fore, Style, Back
    import sys
    

    colorama_init(autoreset=True)
    print(f"{Fore.RED}{Back.GREEN}IPBus interface unit test:")
    ipBus = IPBus()

    print()
    ipBus.statusRequest()
    if ipBus.statusResponse() >= 0:
        print(ipBus.status)
        print(f"{Fore.GREEN}Status request success")
    else:
        print(f"{Fore.RED}Status request failed")
        sys.exit(1)


    save = 0x16
    status = ipBus.write(0x1004, save, False)
    if status >= 0:
        print(f"{Fore.GREEN}Write success")
        print(TransactionInfoCodeStringType[status])
    else:
        print(f"{Fore.RED}Write failed")
        sys.exit(1)


    status, data = ipBus.read(0x1004, 1, False)
    if status >= 0 and data[0] == save:
        print(f"{Fore.GREEN}Read success")
        print(f"Read data: {data}")
    else:
        print(f"{Fore.RED}Read failed")
        sys.exit(1)

    ipBus.write(0x1004, 0xFFFF0000, False)
    ipBus.readModifyWriteBits(0x1004, 0xFF00_0000, 0xFF)
    status, data = ipBus.read(0x1004, 1, False)
    if status >= 0 and data[0] == 0xFF0000FF:
        print(f"{Fore.GREEN}ReadModifyWriteBits success")
        print(f"Read data: {data}")
    else:
        print(f"{Fore.RED}ReadModifyWriteBits failed")
        print(f"Read data: {data}")
        sys.exit(1)

    
    ipBus.write(0x1004, 0x01, False)
    ipBus.readModifyWriteSum(0x1004, 0x10)
    status, data = ipBus.read(0x1004, 1, False)
    if status >= 0 and data[0] == 0x11:
        print(f"{Fore.GREEN}ReadModifyWriteSum success")
        print(f"Read data: {data}")
    else:
        print(f"{Fore.RED}ReadModifyWriteSum failed")
        sys.exit(1)



    ipBus.write(0x1004, [0x01, 0x02], False)
    status, data = ipBus.read(0x1004, 2, False)
    if status >= 0 and data == [0x01, 0x02]:
        print(f"{Fore.GREEN}Read success")
        print(f"Read data: {data}")
    else:
        print(f"{Fore.RED}Read failed")
        sys.exit(1)

    
    print(f"{Fore.GREEN}Unit test success")
