import socket
import csv
address = ('192.168.192.66', 8000)

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind(address)




file_name = f"temp.txt"
#csv_writer = csv.writer(fd. delimiter=',')

def receive_data() -> str:
    msg ,_ = server_sock.recvfrom(1000)
    print("Message received!")
    print(msg)
    time, temp, hum = msg.decode().split(',')
    print(f" Time: {time} || Temp: {temp} °C || Humidity: {hum} % ")
    return msg.decode()

with open(file_name, "w") as fd:
    while True:
        msg = receive_data()
        print("Writing data")
        fd.write(f"{msg}\n")
