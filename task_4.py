"""
Что нужно сделать
Ваш коллега, применив JsonAdapter из предыдущей задачи,
сохранил логи работы его сайта за сутки в файле skillbox_json_messages.log.
Помогите ему собрать следующие данные:

Сколько было сообщений каждого уровня за сутки.
В какой час было больше всего логов.
Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
Сколько сообщений содержат слово dog.
Какое слово чаще всего встречалось в сообщениях уровня WARNING.
Советы и рекомендации

Для поверхностного анализа логов нередко используют grep— встроенную утилиту Linux.
Например, с её помощью можно посчитать количество логов уровня ERROR:
$ grep -c '"level": "ERROR"' skillbox_json_messages.log
3951
Или получить логи в период с 17:10:00 до 17:10:09:
$ grep '"time": "17:10:0' skillbox_json_messages.log
{"time": "17:10:00", "level": "DEBUG", "message": "scurvy's …"}
{"time": "17:10:06", "level": "ERROR", "message": "careless …"}


Попробуйте решить задачи 3 и 4 с помощью этой утилиты.
Для группировки данных удобно использовать функцию itertools.groupby.
Она может пригодиться, например, для группировки логов по часам.


Что оценивается
Файл с логами считывается только один раз.
Программа работает с десериализованным JSON.
Сначала происходит фильтрация нужных логов, а только потом анализ.
Решение каждой подзадачи работает не более чем за O(N).

"""

import json
from collections import Counter

level_counter = Counter()
hour_counter = Counter()
critical_logs_counter = 0
dog_counter = 0
warning_words_counter = Counter()

with open('skillbox_json_messages.log', encoding='Windows-1251') as f:
    for line in f:
        log = json.loads(line)
        level = log['level']
        level_counter[level] += 1

        hour = log['time'][:2]
        hour_counter[hour] += 1

        if level == 'CRITICAL' and '05:00:00' <= log['time'] <= '05:20:00':
            critical_logs_counter += 1

        if 'dog' in log['message']:
            dog_counter += 1

        if level == 'WARNING':
            words = log['message'].split()
            warning_words_counter.update(words)

print('Messages of each level per day:')
for lev, cnt in level_counter.items():
    print(f'{lev}: {cnt}')

max_hour, max_hour_count = hour_counter.most_common(1)[0]
print(f'\nMost logs in {max_hour} hour: {max_hour_count}')

print(f'\nCRITICAL  05:00:00 till 05:20:00: {critical_logs_counter}')

print(f'\nMessages containing "dog": {dog_counter}')

if warning_words_counter:
    most_common_word, times = warning_words_counter.most_common(1)[0]
    print(f'\nThe most common word in WARNING: "{most_common_word}" ({times} times)')
else:
    print('\nВ WARNING no words found')
