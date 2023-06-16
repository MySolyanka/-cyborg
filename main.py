import telebot
import requests
import os
import mimetypes
# Создаем экземпляр бота
bot = telebot.TeleBot('6062432681:AAEV0hQgLkffqo5qv1WTJ9z138pyQ6mNBUQ')


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "/start":
        # Приветствие и вопрос пользователя
        bot.send_message(message.chat.id, "Привет!")
    elif message.text.startswith('/check_message'):
        topic = message.text.replace('/check_message', '').strip()

        # URL вашего backend'а

        respons_url = "http://localhost:8000/api/bot/{topic}".format(topic=topic)
        # Выполнение GET-запроса
        response = requests.get(respons_url)

        # Проверка статуса ответа
        if response.status_code == 200:
            # Запрос успешен
            data = response.json()

            # Проверка наличия записи в базе данных
            if data["found"]:
                # Отправка сообщения ботом
                bot.send_message(message.chat.id, data["message"])

                # Проверка наличия ID файла
                if "id" in data:
                    print(data)
                    file_id = data["id"]
                    file_url = "http://localhost:8000/api/data/{id}/download".format(id=file_id)
                    print(file_url)
                    # Запрос для скачивания файла
                    file_response = requests.get(file_url)

                    # Проверка статуса ответа при скачивании файла
                    if file_response.status_code == 200:
                        content_type = file_response.headers.get('Content-Type', '')
                        extension = mimetypes.guess_extension(content_type) if '/' in content_type else ''
                        # Сохранение файла на сервере
                        file_path = 'downloaded_file' + extension
                        with open(file_path, 'wb') as file:
                            file.write(file_response.content)

                        # Отправка файла ботом
                        with open(file_path, 'rb') as file:
                            bot.send_document(message.chat.id, file)

                        # Удаление временного файла
                        os.remove(file_path)
                    else:
                        # Ошибка при скачивании файла
                        bot.send_message(message.chat.id, "Ошибка при скачивании файла.")
            else:
                # Запись не найдена
                bot.send_message(message.chat.id, "Запись не найдена.")
        else:
            # Обработка ошибки
            bot.send_message(message.chat.id, "Ошибка при выполнении запроса.")

    # Возвращаемся в начало
    bot.send_message(message.chat.id, "Что вас интересует?")


# Запускаем бота
bot.polling()