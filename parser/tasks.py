from celery import shared_task
import logging
from .parser import run_parsing

logger = logging.getLogger(__name__)

@shared_task
def run_parser_task():
    logger.info('Парсер запускается.')
    try:
        run_parsing()
        logger.info('Парсер завершил работу.')
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")


@shared_task
def test_task():
    return 'Задача выполнена успешно!'