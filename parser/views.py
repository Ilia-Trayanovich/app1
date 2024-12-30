from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
import subprocess
from django.contrib import messages
from .tasks import run_parser_task


# Проверка, что пользователь является администратором
def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def run_parser_view(request):
    if request.method == "POST":
        try:
            # Запускаем задачу в Celery
            task = run_parser_task.delay()

            # Получаем результат (если нужно, можно использовать task.id для проверки статуса)
            messages.success(request, "Парсер запущен в фоновом режиме.")
        except Exception as e:
            messages.error(request, f"Ошибка: {str(e)}")

    return render(request, 'parser/run_parser.html')