""" Задача 3. JSON-логирование
Что нужно сделать
Удобно сохранять логи в определённом формате, чтобы затем их можно было фильтровать и анализировать. Сконфигурируйте логгер так, чтобы он писал логи в файл skillbox_json_messages.log в следующем формате:

{"time": "<время>", "level": "<уровень лога>", "message": "<сообщение>"}
Но есть проблема: если в message передать двойную кавычку, то лог перестанет быть валидной JSON-строкой:

{"time": "21:54:15", "level": "INFO", "message": }
Чтобы этого избежать, потребуется LoggerAdapter. Это класс из модуля logging, который позволяет модифицировать логи перед тем, как они выводятся.

У него есть единственный метод — process, который изменяет сообщение или именованные аргументы, переданные на вход.

class JsonAdapter(logging.LoggerAdapter):
def process(self, msg, kwargs):
# меняем msg
return msg, kwargs
Использовать можно так:

logger = JsonAdapter(logging.getLogger(__name__))
logger.info('Сообщение')
Вам нужно дописать метод process так, чтобы в логах была всегда JSON-валидная строка.

Советы и рекомендации
LoggerAdapter Objects.
Обратите внимание: кавычки нужно экранировать, а не удалять или заменять на другие. Помимо кавычек есть и другие тонкости, например переносы строк. Чтобы всё учесть, воспользуйтесь методом json.dumps.
 """

import logging
import json
from datetime import datetime


class JsonAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        log_record = {
            'time': datetime.now().strftime('%H:%M:%S'),
            'level': kwargs.get('level', self.extra.get('level', '')) or self.logger.level,
            'message': msg
        }

        json_msg = json.dumps(log_record, ensure_ascii=False)
        return json_msg, {}


logging.basicConfig(
    level=logging.INFO,
    filename='skillbox_json_messages.log',
    filemode='a',
    encoding='Windows-1251',
    format='%(message)s'
)

logger = JsonAdapter(logging.getLogger(__name__), {})

logger.info('Message with "quotes" and \nline breaks')
