import telebot

from config import TOKEN
from utils import keys
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)




@bot.message_handler(commands=['start', 'help'])
def echo_test(message: telebot.types.Message):
    text = '''Бот возвращает цену на определенное количество одной валюты в другой валюте. 
    
    Чтобы начать работу введите комманду боту в следующем формате: \n 
    <имя валюты, цену которой он хочет узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>. \n 
    Чтобы увидеть список всех доступных валют введите команду: /values '''

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))

    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Неверное количество параметров')

        base, quote, amount = values
        total = Converter.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        # print(e)
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Цена {amount} {base} в валюте {quote} составляет {total}'
        bot.send_message(message.chat.id, text)










bot.polling()
