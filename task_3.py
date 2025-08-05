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
    encoding='utf-8',
    format='%(message)s'
)

logger = JsonAdapter(logging.getLogger(__name__), {})

logger.info('Сообщение с "кавычками" и переносом \nстроки')
