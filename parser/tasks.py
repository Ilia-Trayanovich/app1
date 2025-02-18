from celery import shared_task
import logging
from .parser import run_parsing
from analytics.utils import generate_graphs

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


@shared_task
def generate_graphs_task():
    logger.info('Графики создаются.')
    try:
        generate_graphs()
        logger.info('Графики успешно созданы.')
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
