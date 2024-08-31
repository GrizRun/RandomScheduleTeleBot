import threading
import time
import queue
from reminder_bot import run_bot
from schedule import Schedule

if __name__ == "__main__":
    reminder_queue = queue.Queue()  # Канал для отправки событий
    response_queue = queue.Queue()  # Канал для получения ответов

    schedule = Schedule('events.json', reminder_queue, response_queue)

    """
    while True:
        time.sleep(1)  # Ждем 15 секунд перед отправкой ответа
        if not reminder_queue.empty():
            event = reminder_queue.get()
            print(f"Ответ получен на событие: {event.text} (Заголовок: {event.title})")
            response_queue.put(event)  # Отправляем ответ в канал
    """

    run_bot(reminder_queue, response_queue)

    print("what?")
    while True:
        time.sleep(1)  # Держим основной поток активным
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
