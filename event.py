import time
import random
from datetime import datetime, timedelta



class Event:
    def __init__(self, title, frequency, text='', deviation_rate=20, next_call=None):
        """
        Инициализация события.

        :param title: Название события
        :param frequency: Частота в секундах
        :param text: Текст сообщения для отправки
        :param deviation_rate: процент отклонения
        :param next_call: следующий вызов

        """
        self.title = title
        self.frequency = frequency
        self.text = text
        self.deviation_rate = deviation_rate
        ### Создаём следующий вызов
        if next_call is None:
            self.make_new_call()
        else:
            self.next_call = datetime.strptime(next_call, "%Y-%m-%dT%H:%M:%S.%f")

    def make_new_call(self):
        """
        Получить время напоминания со случайным отклонением.

        :return: Время напоминания (datetime)
        """
        deviation = 1 - random.randint(-self.deviation_rate, self.deviation_rate) / 100
        self.next_call = datetime.now() + timedelta(seconds = deviation * self.frequency * 24 * 60 * 60)

    ### определяем сравнение для сортировки
    def __lt__(self, other):
        return self.next_call < other.next_call

    def get_next_call(self):
        """
        вернуть следующий вызов
        """
        return self.next_call

    def to_dict(self):
        return {
            "title": self.title,
            "frequency": self.frequency,
            "text": self.text,
            "deviation_rate": self.deviation_rate,
            "next_call": self.next_call.isoformat() if isinstance(self.next_call, datetime) else self.next_call
        }
