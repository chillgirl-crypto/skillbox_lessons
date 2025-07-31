import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)  # уровень INFO и выше

file_handler = logging.FileHandler('stderr.txt', mode='a', encoding='utf-8')

formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s: %(message)s',
                              datefmt='%H:%M:%S')

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.debug("Это debug-сообщение (не будет выведено)")
logger.info("Это info-сообщение")
logger.warning("Это warning-сообщение")
logger.error("Это error-сообщение")
