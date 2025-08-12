"""Задача 1. Аутентификация
Что нужно сделать
Сконфигурируйте логгер программы из темы 4 так, чтобы он:

писал логи в файл stderr.txt;
не писал дату, но писал время в формате HH:MM:SS, где HH — часы, MM — минуты, SS — секунды с ведущими нулями. Например, 16:00:09;
выводил логи уровня INFO и выше.
Советы и рекомендации
 Уровни логов.

Что оценивается
Логи записываются в файл stderr.txt.
Время отображается с ведущими нулями."""

import logging
import json
from datetime import datetime


class JsonAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        level = kwargs.pop('level', None)
        if level is None:
            level = logging.getLevelName(self.logger.level)
        log_record = {
            'time': datetime.now().strftime('%H:%M:%S'),
            'level': level,
            'message': msg
        }

        json_msg = json.dumps(log_record, ensure_ascii=False)
        return json_msg, kwargs


logging.basicConfig(
    level=logging.INFO,
    filename='skillbox_json_messages.log',
    filemode='a',
    encoding='utf-8',
    format='%(message)s'
)

logger = JsonAdapter(logging.getLogger(__name__), {})

logger.info('This is a "text" message with quotes and \nline breaks!')
logger.warning('Warning: check the data.')
