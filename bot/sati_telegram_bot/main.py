import telebot
import threading
import ambient
import time

API_KEY = "5961423589:AAHwZ567FyqAFMZRUvjABNFWKPVXGjAlWnA"

bot = telebot.TeleBot(API_KEY)


old_temp = 0
old_hum = 0
old_co2 = 0

chat_id = 0

def check_ambient():
    global old_temp, old_hum, old_co2
    while True:
        new_data = ambient.new_data()
        if new_data:
            temp = int(ambient.temp())
            hum = int(ambient.humidity())
            co2 = int(ambient.co2())
            if temp > 30 and temp != old_temp:
                bot.send_message(chat_id, "WARNING: Temperature is over safe limits\nTemperature: {}°C".format(temp))
            if hum < 30 and hum != old_hum:
                bot.send_message(chat_id, "WARNIG: Humidity is under safe limits\nHumidity: {}%".format(hum))

            if co2 > 1000 and co2 != old_co2:
                bot.send_message(chat_id, "WARNIG: CO2 concentration is over safe limits\nCO2: {}ppm".format(co2))
            old_temp = temp
            old_hum = hum
            old_co2 = co2
        time.sleep(5)

@bot.message_handler(commands=['status'])
def status(message):
    temp = int(ambient.temp())
    hum = int(ambient.humidity())
    co2 = int(ambient.co2())
    bot.reply_to(message, "Latest Ambient Readings:\nGPS Time: {}, Location: {}\nTemperature: {}°C\nHumidity {}%\nCO2 Concentration: {}ppm".format(ambient.gps_time(),ambient.location(),temp,hum,co2))

@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, "Hello dear fire watcher")

checking = threading.Thread(target=check_ambient, daemon=True)

@bot.message_handler(commands=['start'])
def start(message):
    global chat_id
    chat_id = message.chat.id
    bot.reply_to(message, "Welcome to SATI FireWatch app")
    if not checking.is_alive():
        checking.start()

bot.polling()
