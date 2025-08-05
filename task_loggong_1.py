import logging
import json
from datetime import datetime

class JsonAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        # Получаем уровень лога в виде строки
        # Если в kwargs передан 'level', то используем его; иначе берем у logger
        level = kwargs.pop("level", None)
        if level is None:
            # Преобразуем числовой уровень лога в строку, например "INFO"
            level = logging.getLevelName(self.logger.level)
        log_record = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "level": level,
            "message": msg
        }
        # Преобразуем лог в валидную JSON-строку, экранируя все специальные символы
        json_msg = json.dumps(log_record, ensure_ascii=False)
        return json_msg, kwargs

# Настраиваем логгер
logging.basicConfig(
    level=logging.INFO,
    filename='skillbox_json_messages.log',
    filemode='a',
    encoding='utf-8',  # Очень важно!
    format='%(message)s' # Нам не нужно ничего, кроме нашего сообщения
)

# Создаём экземпляр адаптера
logger = JsonAdapter(logging.getLogger(__name__), {})

# Пример использования
logger.info('Это "тестовое" сообщение с кавычками и переносом\nстроки!')
logger.warning('Warning: проверьте данные.')

# После запуска, строки в skillbox_json_messages.log будут такого вида:
# {"time": "16:40:12", "level": "INFO", "message": "Это \"тестовое\" сообщение с кавычками и переносом\nстроки!"}
# {"time": "16:40:12", "level": "WARNING", "message": "Warning: проверьте данные."}

