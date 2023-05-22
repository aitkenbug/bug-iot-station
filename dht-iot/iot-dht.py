#!/usr/bin/python
import sys
import Adafruit_DHT
from datetime import datetime
from zoneinfo import ZoneInfo
import csv
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_data_with_timeout(data: str, address: tuple[str, int]):
    client_socket.sendto(data.encode(), address)

def get_sensor_data():
    now = datetime.now()
    now = now.strftime("%Y%m%dT%H%M%S")
    humidity, temperature = Adafruit_DHT.read_retry(11,18)
    return now, temperature, humidity

address = ('192.168.192.66', 8000)
now = datetime.now().strftime('%Y%m%dT%H%M')
file_name = f"log-data-{now}.csv"
WELCOME_STR = f"""
Esto es un loger para ver cosas de temperatura y humedad dado una fecha, eso logea al siguiente archivo
         ----> {file_name} <----
Aqui pueden ver los resultados en la misma carpeta donde ejectuaron este script
"""
print(WELCOME_STR)
with open(file_name, "w") as f:
    csv_writer = csv.writer(f, delimiter=',')
    csv_writer.writerow(["fecha", "temp", "hum"])
    while True:
        try:
            data = get_sensor_data()
            csv_writer.writerow(data)
            string_data = '{0},{1:0.1f},{2:0.1f}'.format(data[0],data[1],data[2])
            send_data_with_timeout(string_data, address)

        except KeyboardInterrupt:
            print(f"Programa interrupido! ver {file_name} para los resultados")
            break
