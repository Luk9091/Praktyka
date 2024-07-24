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
    status = StatusPacket()
    _id: int
    
    header: PacketHeader = PacketHeader()
    transaction: TransactionHeader = TransactionHeader(transactionType= 0, nWords=0, id=0)

    def __init__(self, IP_address: str | None = "localhost", IP_port: str | None = 50001):
        if IP_address is not None:
            self.address.IP = IP_address
        if IP_port is not None:
            self.address.port = IP_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(1)

        self._id = 0

    def __del__(self):
        self.socket.close()


    def __writing(self, toSend: list | bytearray) -> bool:
        if not isinstance(toSend, bytearray): toSend = bytearray(toSend)
        n: int = self.socket.sendto(toSend, self.address())
        if (n == -1) or (n != len(toSend)):
            return False

        self._id += 1
        if self._id > 0xFFF:
            self._id = 0
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
                !!! Max read size: 255 words !!!
            Read from register:

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
        packetHeader = PacketHeader(PacketType["control"])
        transaction = TransactionHeader(transactionType, nWords, id=self._id)
        toSend = packetHeader.toBytesArray("little")
        toSend = [*toSend, *transaction.toBytesArray("little")]
        toSend = [*toSend, *startRegisterAddress.to_bytes(4, "little")]

        if not self.__writing(toSend):
            return -1, None

        
        status, data = self.__reading()
        if not status:
            return -1, None

        self.header.fromBytesArray(data[0:4])
        self.transaction.fromBytesArray(data[4:8])

        readWords = []
        for i in range(8, len(data), 4):
            readWords.append(int.from_bytes(data[i:i+4], "little", signed=signed))
        
        return self.transaction.infoCode, readWords

    def write(self, startRegisterAddress: int, data: list[int] | int, FIFO: bool) -> int:
        '''
                !!! Max write size: 255 words !!!
            Write to register:

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
        header = TransactionHeader(transactionType, len(data), id=self._id)
        toSend = packetHeader.toBytesArray("little")
        toSend = [*toSend, *header.toBytesArray("little")]
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

        self.header.fromBytesArray(data[0:4])
        self.transaction.fromBytesArray(data[4:8])
        return self.transaction.infoCode


    def readModifyWriteBits(self, registerAddress: int, ANDmask: int, ORmask: int) -> int:
        '''
            Read-Modify-Write bits in register:
            Y <= (X & ANDmask) | ORmask

            X - value stored in register
            Y - new value stored in register
        '''
        header = TransactionHeader(TransactionType["RMWbits"], 1, id=self._id)
        packetHeader = PacketHeader(PacketType["control"])
        toSend = packetHeader.toBytesArray("little")
        toSend = [*toSend, *header.toBytesArray("little")]
        toSend = [*toSend, *registerAddress.to_bytes(4, "little")]
        toSend = [*toSend, *ANDmask.to_bytes(4, "little")]
        toSend = [*toSend, *ORmask.to_bytes(4, "little")]

        if not self.__writing(toSend):
            return -1, 0

        status, data = self.__reading()
        if not status:
            return -1, 0

        self.header.fromBytesArray(data[0:4])
        self.transaction.fromBytesArray(data[4:8])

        return self.transaction.infoCode, int.from_bytes(data[8:12], "little")

    def readModifyWriteSum(self, registerAddress: int, addend: int, signed_read: bool = False) -> tuple[int, int]:
        '''
            Read-Modify-Write sum in register:
            Y <= X + addend

            X - value stored in register
            Y - new value stored in register
        '''
        signed_add = False
        if addend < 0:
            signed_add = True

        header = TransactionHeader(TransactionType["RMWsum"], 1, id=self._id)
        packetHeader = PacketHeader(PacketType["control"])
        toSend = packetHeader.toBytesArray("little")
        toSend = [*toSend, *header.toBytesArray("little")]
        toSend = [*toSend, *registerAddress.to_bytes(4, "little")]
        toSend = [*toSend, *addend.to_bytes(4, "little", signed=signed_add)]

        if not self.__writing(toSend):
            return -1, 0

        status, data = self.__reading()
        if not status:
            return -1, 0

        self.header.fromBytesArray(data[0:4])
        self.transaction.fromBytesArray(data[4:8])
        return self.transaction.infoCode, int.from_bytes(data[8:12], "little", signed=signed_read)
    
    # @set
    # def timeout(self, value:oat | None):
    #     self.socket.settimeout(value)




if __name__ == '__main__':
    from colorama import init as colorama_init
    from colorama import Fore, Style, Back
    import sys
    
    TEST_REG = 0x1004
    TEST_REG2= 0x1005

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
    status = ipBus.write(TEST_REG, save, False)
    if status >= 0:
        print(f"{Fore.GREEN}Write success")
        print(TransactionInfoCodeStringType[status])
    else:
        print(f"{Fore.RED}Write failed")
        sys.exit(1)


    status, data = ipBus.read(TEST_REG, 1, False)
    if status >= 0 and data[0] == save:
        print(f"{Fore.GREEN}Read success")
        print(f"Read data: {data}")
    else:
        print(f"{Fore.RED}Read failed")
        sys.exit(1)

    ipBus.write(TEST_REG, 0xFFFF0000, False)
    ipBus.readModifyWriteBits(TEST_REG, 0xFF00_0000, 0xFF)
    status, data = ipBus.read(TEST_REG, 1, False)
    if status >= 0 and data[0] == 0xFF0000FF:
        print(f"{Fore.GREEN}ReadModifyWriteBits success")
        print(f"Read data: {data}")
    else:
        print(f"{Fore.RED}ReadModifyWriteBits failed")
        print(f"Read data: {data}")
        sys.exit(1)

    
    ipBus.write(TEST_REG, 0x01, False)
    ipBus.readModifyWriteSum(TEST_REG, 0x10)
    status, data = ipBus.read(TEST_REG, 1, False)
    if status >= 0 and data[0] == 0x11:
        print(f"{Fore.GREEN}ReadModifyWriteSum success")
        print(f"Read data: {data}")
    else:
        print(f"{Fore.RED}ReadModifyWriteSum failed")
        sys.exit(1)



    ipBus.write(TEST_REG, [0x01, 0x02], False)
    status, data = ipBus.read(TEST_REG, 2, False)
    if status >= 0 and data == [0x01, 0x02]:
        print(f"{Fore.GREEN}Read success")
        print(f"Read data: {data}")
    else:
        print(f"{Fore.RED}Read failed")
        sys.exit(1)

    
    print(f"{Fore.GREEN}Unit test success")
