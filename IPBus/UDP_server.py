import socket

# server_address = ("172.20.75.180", 50001)
server_address = ("localhost", 50001)
buffer_size = 368

UDP_serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_serverSocket.bind(server_address)
print("Server is listening")
try:
    while True:
        dataAddressPair = UDP_serverSocket.recvfrom(buffer_size)
        data = dataAddressPair[0]
        address = dataAddressPair[1]

        print("Received data: ", data)
        UDP_serverSocket.sendto(data, address)

        for i in range(0, len(data), 4):
            value = int.from_bytes(data[i:i+4], "little")
            print(f"{int(i/4):2d}: {value:8X}")
except:
    print("Error")
    

UDP_serverSocket.close()
print("Server is closed")

