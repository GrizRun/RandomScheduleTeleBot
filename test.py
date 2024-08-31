import dateparser
import datetime

if __name__ == "__main__":

    # Пример текста
    text = "через 0.00003 дня"

    # Парсинг текста
    time_delta = dateparser.parse(text) - datetime.datetime.now()

    ##time_delta = time_delta * 0.8
    # Получение общего количества секунд
    print(time_delta)