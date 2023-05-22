#!/usr/bin/python
import sys
import Adafruit_DHT
from datetime import datetime
from zoneinfo import ZoneInfo
import csv
import socket


def get_sensor_data():
    now = datetime.now()
    now = now.strftime("%Y%m%dT%H%M%S")
    humidity, temperature = Adafruit_DHT.read_retry(11,18)
    data = 'Time: {0} Temp: {1:0.1f} C  Humidity: {2:0.1f} %'.format(now, temperature, humidity)
    return now, temperature, humidity

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
            string_data = 'Time: {0} Temp: {1:0.1f} C  Humidity: {2:0.1f} %'.format(data[0],data[1],data[2])
            print(string_data)
        except KeyboardInterrupt:
           print(f"Programa interrupido! ver {file_name} para los resultados")
           break
    #send_data(string_data, address)
