import telebot
from config import keys, TOKEN
from extensions import APIException, GetPrice


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, ' + str(message.from_user.first_name) + '✌' + '\n' + 'это криптовалютный бот' + '\n\n' + 'напиши /help, чтобы посмотреть что я умею.')


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'напиши команду боту в следующем формате:\n<количество переводимой криптовалюты>\n<название криптовалюты>\n<в какую криптовалюту перевести>\nпосмотреть список всех доступных криптовалют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'доступные криптовалюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(commands=['other_commands'])
def other(message: telebot.types.Message):
    bot.send_message(message.chat.id, "sorry, i don't understand😐 ")


@bot.message_handler(content_types=['voice'])
def voice_message(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'You have a beautiful voice 😊')


@bot.message_handler(content_types=['photo'])
def text(message: telebot.types.Message):
    bot.send_message(message.chat.id, "great pic! ")


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise APIException('нужно указать только три значения')

        if len(values) < 3:
            raise APIException('нужно указать три параметра')

        amount, quote, base = values
        total_base = GetPrice.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'не удалось обработать команду\n{e}')
    else:
        text = f'{amount} {quote} это {total_base} {base} '
        bot.send_message(message.chat.id, text)


bot.polling()