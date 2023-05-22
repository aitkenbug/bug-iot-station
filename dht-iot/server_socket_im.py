import socket
address = ('localhost', 8000)

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind(address)

file_name = f"temp.csv"
with open(file_name, "rw") as fd:
    ...
