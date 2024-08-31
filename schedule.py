import json
import threading
import time
from event import Event
import queue
from datetime import datetime, timedelta

class Schedule:
    # при инициализации расписание создаётся, поток, который раз в 10 секунд проходит по json
    # если находит событие с пустым next_call, то делает ему next_call и кладёт обратно
    # если находит событие с next_call меньше текущего времени,
        #  проверяет, что по этому событию ещё не отправлялось напоминание
        #  если нет,
            #   то отправляет напоминание-событие
            #  запоминает, что по данному событию было отправленно напоминание
    # закончив обход всех напоминаний проверяет не пришлили в поток обратки по отправленным событиям
        # если пришёл обратный ответ, то
            # удаляет его из списка отправленных
            # кладёт в расписание событие с новой датой next_call
    def __init__(self, filename, reminder_queue, response_queue):
        self.filename = filename
        self.events = self.load_events()  # Изменили на load_events
        self.sent_events = set()  # Множество для хранения отправленных событий
        self.reminder_queue = reminder_queue  # Канал для отправки напоминаний
        self.response_queue = response_queue  # Канал для получения ответов
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def load_events(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return [Event(**item) for item in data]

    def save_events(self):
        events_dict = [event.to_dict() for event in self.events]
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(events_dict, file, ensure_ascii=False, indent=4)

    def run(self):
        while True:
            current_time = datetime.now()
            for event in self.events:
                if event.next_call is None:
                    event.make_new_call()
                elif event.next_call <= current_time and event not in self.sent_events:

                    print(f"Событие  {event.title} время {event.next_call})")
                    self.sent_events.add(event)
                    self.reminder_queue.put(event)
            self.check_responses()
            self.save_events()
            time.sleep(1)

    def send_event(self, event):  # Изменили send_reminder на send_event
        self.reminder_queue.put(event)  # Отправляем событие в канал
        print(f"Событие отправлено: {event.text} (Заголовок: {event.title})")

    def check_responses(self):
        while not self.response_queue.empty():
            event = self.response_queue.get()  # Получаем ответ из канала
            self.sent_events.remove(event)
            event.make_new_call()




