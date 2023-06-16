#!/usr/bin/python
import sys
import Adafruit_DHT
from datetime import datetime
from zoneinfo import ZoneInfo
import csv
import socket
import numpy as np

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

address = ('192.168.192.66', 8000)
now = datetime.now().strftime('%Y%m%dT%H%M')
file_name = f"/var/www/html/dht_data_seconds.csv"


def send_data_with_timeout(data: str, address: tuple[str, int]):
    client_socket.sendto(data.encode(), address)

def get_sensor_data():
    now = datetime.now()
    now = now.strftime("%Y%m%dT%H%M%S")
    humidity, temperature = Adafruit_DHT.read_retry(11,18)
    return now, temperature, humidity

def csv_data_writer(entry, actual_file=file_name):
    with open(actual_file, 'r') as file:
        content = csv.reader(file)
        lines = list(content)
    num_lines = len(lines)
    lines.append(entry)
    if num_lines >= 31:
       lines.pop(1)
    with open(actual_file, 'w', newline='') as file:
        write_content = csv.writer(file)
        write_content.writerows(lines)
    #print('Temporal CSV data updated!!! '+str(datetime.now().strftime("%Y-%m-%d-%H:%M:%S")))

WELCOME_STR = f"""
Esto es un loger para ver cosas de temperatura y humedad dado una fecha, eso logea al siguiente archivo
         ----> {file_name} <----
Aqui se guardan los datos para poder graficarlos en una pagina web
"""
print(WELCOME_STR)

minute_data=[]
hour_data=[]
old_time_minute=datetime.now()
old_time_hour=datetime.now()

with open(file_name, "r") as file:
    content = csv.reader(file)
    lines = list(content)
    num_lines = len(lines)

    if num_lines < 2:
        with open(file_name, "w") as file:
            csv_writer = csv.writer(file, delimiter=',')
            csv_writer.writerow(["fecha", "temp", "hum"])


    while True:
        try:
            data = get_sensor_data()
            csv_data_writer(data)
            minute_data.append(data)
            string_data = '{0},{1:0.1f},{2:0.1f}'.format(data[0],data[1],data[2])
            send_data_with_timeout(string_data, address)

        except KeyboardInterrupt:
            print(f"Programa interrupido! ver {file_name} para los resultados")
            break

        if (datetime.now()-old_time_hour).seconds//60 >= 60:
            temp = []
            hum = []
            for i in hour_data:
                temp.append(float(i[1]))
                hum.append(float(i[2]))
            mean_temperature_min = '%.2f'%np.mean(temp)
            mean_humidity_min = '%.2f'%np.mean(hum)
            temp_data = [hour_data[-1][0], mean_temperature_min, mean_humidity_min]
            with open(f"/var/www/html/dht_data_hour.csv", "w") as file:
                csv_writer = csv.writer(file, delimiter=',')
                csv_writer.writerow(temp_data)
            print('Hour Data CSV Updated Time: {0}\nTemperature: {1}°C\nHumidity: {2} RH%\n'.format(temp_data[0],temp_data[1],temp_data[2]))
            hour_data = []
            old_time_hour = datetime.now()


        if (datetime.now()-old_time_minute).seconds//60 >= 1:
            temp = []
            hum = []
            for i in minute_data:
                temp.append(i[1])
                hum.append(i[2])
            mean_temperature_min = '%.2f'%np.mean(temp)
            mean_humidity_min = '%.2f'%np.mean(hum)
            temp_data = [minute_data[-1][0], mean_temperature_min, mean_humidity_min]
            hour_data.append(temp_data)
            csv_data_writer(temp_data, f"/var/www/html/dht_data_minute.csv")
            print('Minute Data CSV Updated Time: {0}\nTemperature: {1}°C\nHumidity: {2} RH%\n'.format(temp_data[0],temp_data[1],temp_data[2]))
            minute_data=[]
            old_time_minute = datetime.now()


