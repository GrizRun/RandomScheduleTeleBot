import threading
import telebot
import queue
from telebot import TeleBot, types
import time
import json
import event

# Укажите ваш API ключ Telegram
TELEGRAM_API_KEY = "7254672894:AAED6RmJNu0rx32qiOSFkRIcqDX84HCHsmg"

bot = telebot.TeleBot(TELEGRAM_API_KEY)
start_message_queue = queue.Queue()
response_message_queue = queue.Queue()
sent_events = {}


# Функция для отправки напоминания
def listen_event_queue(event_queue, response_queue):
    chat_id = None
    while chat_id is None:
        if not start_message_queue.empty():
            chat_id = start_message_queue.get()
        time.sleep(1)
    cur_event_id = 0
    while True:
        if not event_queue.empty():
            event = event_queue.get()
            sent_events[cur_event_id] = event
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("Да, сделал", callback_data=f"done_{cur_event_id}")
            markup.add(btn1)
            bot.send_message(chat_id, f"Напоминание {event.title}: {event.text}", reply_markup=markup)
            cur_event_id += 1
        if not response_message_queue.empty():
            responsed_event_id = response_message_queue.get()
            response_queue.put(sent_events[responsed_event_id])
            print(sent_events)
            del sent_events[responsed_event_id]


        time.sleep(1)  # Задержка перед отправкой напоминания


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я напомню вам о ваших действиях.")
    start_message_queue.put(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    data = call.data.split('_')
    action = data[0]
    event_id = int(data[1])

    if action == "done":
        print(sent_events)
        response_message_queue.put(event_id)

    # Удаляем сообщение с кнопками после обработки
    bot.delete_message(call.message.chat.id, call.message.message_id)

# Запуск бота
def run_bot(event_queue, response_queue):
    # Запуск потока для обработки сообщений
    threading.Thread(target=listen_event_queue, args=(event_queue, response_queue), daemon=True).start()
    bot.polling(none_stop=True)
