import requests
import telebot
from bs4 import BeautifulSoup
from constants import TOKEN


bot = telebot.TeleBot(TOKEN)


def get_info():
    response = requests.get('https://covid19.who.int/region/euro/country/ua')
    soup = BeautifulSoup(response.content, 'html.parser')
    res = soup.find_all('span')

    idx = None

    for i in res:
        if 'deaths' in str(i):
            idx = res.index(i)

    num = res[idx].text.rstrip(' deaths')

    return num


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Работаю. Напиши любой текст для получения обновления")


@bot.message_handler(func=lambda message: True)
def reply_any(message):
    num = get_info()
    msg = f'Всего смертей от covid-19 в Украине на данный момент: {num}'
    bot.send_message(message.chat.id, text=msg)


bot.polling()
