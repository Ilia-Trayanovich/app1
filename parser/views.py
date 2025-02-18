from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .tasks import run_parser_task
from parser.tasks import generate_graphs_task


def is_admin(user):
    return user.is_staff


@user_passes_test(is_admin)
def run_parser_view(request):
    if request.method == "POST":
        try:
            task = run_parser_task.delay()
            messages.success(request, "Парсер запущен в фоновом режиме.")
        except Exception as e:
            messages.error(request, f"Ошибка: {str(e)}")
        try:
            task = generate_graphs_task.delay()
            messages.success(request, "Графики создаются в фоновом режиме.")
        except Exception as e:
            messages.error(request, f"Ошибка: {str(e)}")

    return render(request, "parser/run_parser.html")
