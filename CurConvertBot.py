import telebot
from config import keys, TOKEN
from extensions import ConversionException, CurConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', ])
def start(message: telebot.types.Message):
    text = "Чтобы начать наботу, введите боту команду в таком формате:\nВалюта1 Валюта2 " \
           "Количество " \
           "\nУвидеть список доступных валют /values\n" \
           "Подробнее в инструкции /help"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help', ])
def info(message: telebot.types.Message):
    text = 'Вы можете ознакомиться со списком доступных валют командой /values\n' \
           'Воодите валюты так, как они указаны в списке /values\n' \
           'Введите валюту, которую хотите конвертировать, через пробел ' \
           'валюту, в которую хотите конвертировать, и через пробел количество ' \
           'конвертируемой валюты\n' \
           'Например:\n' \
           'доллар рубль 1\n' \
           'Таким образом, вы узнаете сколько сегодня стоит 1 доллар в рублях'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        get = message.text.split(' ')
        currencies = list((map(str.lower, get)))
        if len(currencies) != 3:
            raise ConversionException('Неверное количество параметров, смотрите инструкцию /help')

        quote, base, amount = currencies
        total = CurConverter.get_price(quote, base, amount)
    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя: \n {e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду: \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total}'
        bot.send_message(message.chat.id, text)


bot.polling()
