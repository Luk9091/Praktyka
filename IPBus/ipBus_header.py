maxWordsPerPacket = 368


PacketType = {
    "control"   : 0,
    "status"    : 1,
    "resend"    : 2
}

TransactionType = {
    "read"                  : 0,
    "write"                 : 1,
    "nonIncrementingRead"   : 2,
    "nonIncrementingWrite"  : 3,
    "RMWbits"               : 4,
    "RMWsum"                : 5,
    "configurationRead"     : 6,
    "configurationWrite"    : 7
}

TransactionInfoCodeStringType = {
            0x0: "Successful request",
            0x1: "Bad header",
            0x4: "IPbus read error",
            0x5: "IPbus write error",
            0x6: "IPbus read timeout",
            0x7: "IPbus write timeout",
            0xf: "outbound request",
            -1 : "unknown Info Code"
}

class PacketHeader:
    packetType: int                                                         # 4 bits
    byteOrder: int = 0xF                                                    # 4 bits
    packetID: int                                                           # 16 bits
    rsvd: int = 0x0                                                         # 4 bits
    protocolVersion: int  = 2                                               # 4 bits

    def __init__(self, packetType: int = PacketType["status"], id: int = 0, bytesArray: bytearray = None) -> None:
        if bytesArray is not None:
            self.fromBytesArray(bytesArray)
        else:
            self.packetType = packetType
            self.packetID = id

    def toBytesArray(self, endian: str = "big") -> bytearray:
        data = self.protocolVersion << 28 | self.rsvd << 24 | self.packetID << 8 | self.byteOrder << 4 | self.packetType
        return bytearray(int(data).to_bytes(4, endian))

    def fromBytesArray(self, data: bytearray) -> None:
        self.protocolVersion    = data[0] >> 4 & 0xF
        self.rsvd               = data[0] & 0xF
        self.packetID           = data[1] << 8 | data[2]
        self.byteOrder          = data[3] >> 4 & 0xF
        self.packetType         = data[3] & 0xF

    def __str__(self) -> str:
        string = f"PacketType: {self.packetType},\n"
        string += f"byteOrder: {self.byteOrder},\n"
        string += f"packetID: {self.packetID},\n"
        string += f"protocolVersion: {self.protocolVersion}"
        return string


class TransactionHeader:
    protocolVersion: int = 2                                                # 4 bits
    transactionID: int                                                      # 12 bits
    words: int                                                              # 8 bits
    typeID: int                                                             # 4 bits
    infoCode: int = 0xF                                                     # 4 bits

    def __init__(self, transactionType: int = None, nWords: int = None, id: int = 0, bytesArray: bytearray = None) -> None:
        if bytesArray is not None:
            self.fromBytesArray(bytesArray)
        elif transactionType is not None and nWords is not None:
            self.typeID = transactionType
            self.words = nWords
            self.transactionID = id
        else:
            raise ValueError("TransactionHeader: Wrong arguments")


    def infoCodeString(self) -> str:
        if (self.infoCode in TransactionInfoCodeStringType):
            return TransactionInfoCodeStringType[self.infoCode]
        else:
            return TransactionInfoCodeStringType[-1]
    
    def toBytesArray(self, endian: str = "little"):
        data = self.protocolVersion << 28 | self.transactionID << 16 | self.words << 8 | self.typeID << 4 | self.infoCode
        return bytearray(int(data).to_bytes(4, endian))

    
    def fromBytesArray(self, data: bytearray) -> None:
        self.protocolVersion =  data[3] >> 4 & 0xF
        self.transactionID   = (data[3] & 0xF) << 8 | data[2]
        self.words           =  data[1]
        self.typeID          =  data[0] >> 4 & 0xF
        self.infoCode        =  data[0] & 0xF

    def __str__(self) -> str:
        string = f"protocolVersion: {self.protocolVersion},\n"
        string += f"transactionID: {self.transactionID},\n"
        string += f"words: {self.words},\n"
        string += f"typeID: {self.typeID},\n"
        string += f"infoCode: {self.infoCode}"
        return string

        

class StatusPacket():
    '''
    Status Packet default values:
        packetHeader: PacketHeader(PacketType["status"])
        MTU: 0
        nResponseBuffers: 0
        nextPacketID: 0
        trafficHistory: [0] * 16
        controlHistory: [0] * 8
    
    Size: 16 words 32bits

    '''

    packetHeader: PacketHeader = PacketHeader(PacketType["status"]) #uint 32
    MTU: int = 0                                                 #uint 32
    nResponseBuffers: int  = 0                                   #uint 32
    nextPacketID: int = 0                                        #uint 32
    trafficHistory: list[bytes, 16] = [0] * 16                   #uint 8 * 16
    controlHistory: list[int, 8] = [0] * 8                       #uint 32 * 8
                                                          # Sum: 16 words 32b

    def toBytesArray(self) -> bytearray:
        byte = []
        byte = [*byte, *self.packetHeader.toBytesArray("big")]
        byte = [*byte, *self.MTU.to_bytes(4, "big")]
        byte = [*byte, *self.nResponseBuffers.to_bytes(4, "big")]
        byte = [*byte, *self.nextPacketID.to_bytes(4, "big")]
        for value in self.trafficHistory:
            byte.append(value)
        for value in self.controlHistory:
            byte = [*byte, *value.to_bytes(4, "big")]
        return bytearray(byte)

    def fromBytesArray(self, data) -> None:
        self.packetHeader.fromBytesArray(data[0:4])
        self.MTU                = int.from_bytes(data[4:8], "big")
        self.nResponseBuffers   = int.from_bytes(data[8:12], "big")
        self.nextPacketID       = int.from_bytes(data[12:16], "big")
        for i in range(16):
            self.trafficHistory[i] = data[16+i]
        for i in range(8):
            self.controlHistory[i] = int.from_bytes(data[32+i*4 : 32 + (i+1)*4], "big")

    def __str__(self) -> str:
        string = f"PacketHeader: \n{self.packetHeader}\n"
        string += f"MTU: {self.MTU}\n"
        string += f"nResponseBuffers: {self.nResponseBuffers}\n"
        string += f"nextPacketID: {self.nextPacketID}\n"
        string += f"trafficHistory: {self.trafficHistory}\n"
        string += f"controlHistory: {self.controlHistory}"

        return string




if __name__ == '__main__':
    print("It is NOT a main module!")
    # statusPacket = StatusPacket()
    # print(statusPacket.toBytes())


    # maxWordsPerPacket = 10
    # print(maxWordsPerPacket)
    # value : list[int] = [0, 1]
    # print(value)


    # print(PacketType["control"])
    # print(PacketType["status"])
    # print(PacketType["resend"])

    # print("PacketHeader:")
    # packetHeader = PacketHeader(PacketType["status"], 0)
    # print(packetHeader)
    # data: int = int(packetHeader)
    # print(hex(data))


    # print("TransactionHeader:")
    # transactionHeader = TransactionHeader(TransactionType["read"], 0x10, 0)
    # print(hex(int(transactionHeader)))
    # print(transactionHeader.infoCodeString())


    # print("StatusPacket:")
    # statusPacket = StatusPacket()
    # print(hex(int(statusPacket.packetHeader)))
    # print(statusPacket.MTU)
    # print(statusPacket.nResponseBuffers)
    # print(statusPacket.nextPacketID)
    # print(statusPacket.trafficHistory)
    # print(statusPacket.controlHistory)