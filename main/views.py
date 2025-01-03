from django.http import HttpResponse
from django.shortcuts import render


def index(request):

    context = {
        "title": "Home - Главная",
        "content": "Продажа квартир. Минск",
    }

    return render(request, "main/index.html", context)


def about(request):
    context = {
        "title": "Home - О нас",
        "content": "О нас",
        "text_on_page": "Текст о том, какой замечательный магазин и прекрасный товар",
    }

    return render(request, "main/about.html", context)
