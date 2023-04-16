import telebot
bot = telebot.TeleBot('6274878724:AAFOD5nXOZFqYi_gZY8kDM_dPXmKHc5v47M')

# Приём сообщений и их обработка
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    match message.text:
        case "Рабочая программа":
            bot.send_message(message.from_user.id, "Тут могла быть рабочая программа")
        case "Лекции":
            bot.send_message(message.from_user.id, "Тут могла быть лекции")
        case "КТП":
            bot.send_message(message.from_user.id, "Тут могло быть КТП")
        case "лабораторные работы по дисциплине name":
            bot.send_message(message.from_user.id, "Тут могли быть лабораторные работы по дисциплине name")
        case "Расписание":
            bot.send_message(message.from_user.id, "Тут могло быть расписание?")

bot.polling(none_stop=True, interval=0)