""" Задача 5. Измерение времени
Что нужно сделать
Каждый лог содержит в себе метку времени, а значит, правильно организовав логирование,
 можно отследить, сколько времени выполняется функция.

Напишите программу,  в файле measure_me.py, по умолчанию пишет логи в stdout.
Внутри неё есть функция measure_me, в начале и в конце которой пишется "Enter measure_me"  и "Leave measure_me" .

Сконфигурируйте логгер, запустите программу,
соберите логи и посчитайте среднее время выполнения функции measure_me.

Что оценивается
Для расчёта времени работы функции используются только данные, предоставленные логами.
В логах используются не только секунды, но и миллисекунды."""

import logging
import time
from datetime import datetime
import sys

""" Кастомный форматтер, который добавляет миллисекунды в asctime """


class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        t = time.strftime("%Y-%m-%d %H:%M:%S", ct)
        s = "%s.%03d" % (t, record.msecs)
        return s


def setup_logger():
    logger = logging.getLogger("measure")
    logger.setLevel(logging.INFO)

    """ Убираем все предыдущие обработчики, если есть """
    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)  # По умолчанию пишем в stdout
    formatter = CustomFormatter('%(asctime)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    """  Не передаём сообщения вверх к root, чтобы не дублировалось """
    logger.propagate = False
    return logger


def measure_me(logger):
    logger.info('Enter measure_me')
    time.sleep(0.2)
    logger.info('Leave measure_me')


def main():
    logger = setup_logger()
    number_of_calls = 5
    """  Временное хранилище логов для анализа """
    records = []

    """ Добавляем свой обработчик, чтобы собирать логи в память параллельно со stdout """
    import io
    stream = io.StringIO()
    memory_handler = logging.StreamHandler(stream)
    memory_handler.setFormatter(CustomFormatter('%(asctime)s %(message)s'))
    logger.addHandler(memory_handler)

    for _ in range(number_of_calls):
        measure_me(logger)
    logger.removeHandler(memory_handler)

    """ Анализ логов """
    log_lines = stream.getvalue().splitlines()
    enter_times = []
    leave_times = []
    for line in log_lines:
        if 'Enter measure_me' in line:
            timestamp = line.split(' Enter')[0].strip()
            enter_times.append(datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f'))
        elif 'Leave measure_me' in line:
            timestamp = line.split(' Leave')[0].strip()
            leave_times.append(datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f'))

    durations = [(leave - enter).total_seconds() for enter, leave in zip(enter_times, leave_times)]
    average = sum(durations) / len(durations) if durations else 0

    print('Execution times:', [f'{d:.6f} с' for d in durations])
    print(f'Average execution time: {average:.6f} с')


if __name__ == '__main__':
    main()
