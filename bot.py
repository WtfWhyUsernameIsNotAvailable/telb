import os
import telebot

# Получаем токен и ID админа из переменных окружения
TOKEN = os.environ["8434031550:AAHNBoj-YMo1F9EIEuZypGDc7ofPPeK2rco"]
ADMIN_ID = int(os.environ["2129917105"])

bot = telebot.TeleBot(TOKEN, parse_mode=None)

# Словарь, чтобы помнить, куда нужно отправить ответ
pending_replies = {}

@bot.message_handler(func=lambda m: m.text and m.text.startswith("!c "))
def handle_command(message):
    text_to_send = message.text[3:].strip()
    chat_id = message.chat.id

    # Запоминаем, откуда пришёл запрос
    pending_replies[ADMIN_ID] = (chat_id, message.message_id)

    # Отправляем админу запрос
    bot.send_message(
        ADMIN_ID,
        f"Запрос из чата {chat_id}:\n{text_to_send}"
    )

@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID)
def handle_admin_reply(message):
    if ADMIN_ID not in pending_replies:
        bot.send_message(ADMIN_ID, "Нет активных запросов для ответа.")
        return

    chat_id, original_msg_id = pending_replies.pop(ADMIN_ID)

    # Отправляем ответ в тот чат, откуда пришла команда
    bot.send_message(chat_id, message.text, reply_to_message_id=original_msg_id)

print("Бот запущен...")
bot.polling(none_stop=True)
