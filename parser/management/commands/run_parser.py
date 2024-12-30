from django.core.management.base import BaseCommand
from parser import parser  # Импортируем парсер из parser.py

class Command(BaseCommand):
    help = 'Запуск парсера'

    def handle(self, *args, **options):
        self.stdout.write("Запуск парсера...")
        
        try:
            # Запуск парсинга
            parser.run_parsing()  # Здесь вызываем функцию из parser.py, которая запускает сам парсер
            self.stdout.write("Парсер завершил работу.")
        except Exception as e:
            self.stderr.write(f"Произошла ошибка при запуске парсера: {e}")
