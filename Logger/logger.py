import socket
import time
import IPBus
import threading
from queue import Queue
from pathlib import Path
from typing import Literal
import sys
import netifaces as ni


class IPBus_logger:
    address: IPBus.ADDRESS
    recv_queue: Queue[tuple[time.struct_time, str, bytearray]]
    running: bool = True
    path: Path

    def __init__(self, ip: str = "localhost", port: int = 50001):
        self.address = IPBus.ADDRESS(ip, port)
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.address())
        # self.socket.settimeout(1)

        self.recv_queue = Queue()
        self.listen_thread = threading.Thread(target= self.__listen)

        
        start_seq = "IPBus_log-"
        current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        self.path = Path(f"./Logs/{start_seq}{current_time}.log")
        self.makeNewDirectory(self.path.parent)


    def __del__(self):
        self.running = False
        try:
            self.socket.shutdown(socket.SHUT_RD)
        except OSError:
            pass
        self.listen_thread.join()
        self.socket.close()


    def __listen(self):
        while self.running:
            try:
                data, address = self.socket.recvfrom(IPBus.maxWordsPerPacket)
            except TimeoutError:
                continue
            
            self.recv_queue.put((time.localtime(), address, data))
    

    def transactionRequest(self, 
            typeID: int | Literal[
                "read",
                "write",
                "nonIncrementingRead",
                "nonIncrementingWrite",
                "RMWbits",
                "RMWsum",
                "configurationRead",
                "configurationWrite"
            ],
            address: tuple[str, int], data_len: int, id: int
        ):

        if isinstance(typeID, str):
            typeID = IPBus.TransactionType[typeID]
        
        header: IPBus.PacketHeader = IPBus.PacketHeader(packetType=IPBus.PacketType["control"], id=0)
        transaction = IPBus.TransactionHeader(
            transactionType = typeID,
            nWords = data_len,
            id = id
        )
        transaction.infoCode = 0
        toSend = header.toBytesArray()
        toSend = [*toSend, *transaction.toBytesArray()]

        if typeID == IPBus.TransactionType["read"] or typeID == IPBus.TransactionType["nonIncrementingRead"]:
            for i in range(data_len):
                toSend = [*toSend, *i.to_bytes(4, "little")]
        elif typeID == IPBus.TransactionType["write"] or typeID == IPBus.TransactionType["nonIncrementingWrite"]:
            pass
        elif typeID == IPBus.TransactionType["RMWbits"] or typeID == IPBus.TransactionType["RMWsum"]:
            value = 0
            toSend = [*toSend, *value.to_bytes(4, "little")]




        self.socket.sendto(bytearray(toSend), address)

    def makeNewDirectory(self, path: Path):
        if not path.exists():
            path.mkdir()

    def writeToFile(self, time, address, data):
        out = f"{time},{address[0]},{address[1]},"
        for i in data:
            out += f"{i},"
        out += "\n"
        with open(self.path, "a") as file:
            file.write(out)
            

    def run(self):
        print("Logger is running...")
        print(f"Listening on {self.address()}")
        self.listen_thread.start()

        while self.running:
            if not self.recv_queue.empty():
                data = []
                local_time, address, rawData = self.recv_queue.get()
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)

                header = IPBus.PacketHeader().fromBytesArray(rawData[0:4])
                transaction = IPBus.TransactionHeader(bytesArray = rawData[4:8])

                for i in range(8, len(rawData), 4):
                    data.append(int.from_bytes(rawData[i:i+4], "little"))

                self.transactionRequest(transaction.typeID, address, transaction.words, transaction.transactionID)

                print(f"{current_time}: {address} -> {data}")
                self.writeToFile(current_time, address, data)

            time.sleep(0.1)
        

    def close(self):
        self.__del__()

def argsToParams(args: list):
    ip = "localhost"
    port = 50001

    if "--ip" in args:
        ip = args[args.index("--ip") + 1]
    elif "--eth" in args:
        eth = args[args.index("--eth") + 1]
        ip = ni.ifaddresses(eth)[ni.AF_INET][0]['addr']
    if "--port" in args:
        port = int(args[args.index("--port") + 1])

    return ip, port


if __name__ == "__main__":
    args = sys.argv[1:]
    ip, port = argsToParams(args)
    logger = IPBus_logger(ip, port)
    try:
        logger.run()
    except KeyboardInterrupt:
        logger.close()