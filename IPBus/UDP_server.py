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
except:
    print("Error")
    

UDP_serverSocket.close()
print("Server is closed")

