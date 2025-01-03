from django.shortcuts import render
from django.template import context
from django.utils import timezone
from datetime import timedelta

from .models import Flats


def catalog(request):
    # Начальные параметры фильтрации
    apartments = Flats.objects.all()

    # Получение параметров фильтрации
    rooms = request.GET.get("rooms")
    min_size = request.GET.get("min_size")
    max_size = request.GET.get("max_size")
    order_by = request.GET.get("order_by", "default")

    # Применение фильтрации по количеству комнат
    if rooms:
        apartments = apartments.filter(rooms=rooms)

    # Применение фильтрации по размеру квартиры
    if min_size:
        apartments = apartments.filter(apartment_size__gte=min_size)
    if max_size:
        apartments = apartments.filter(apartment_size__lte=max_size)

    # Сортировка по цене
    if order_by == "price":
        apartments = apartments.order_by("price")
    elif order_by == "-price":
        apartments = apartments.order_by("-price")

    # Фильтрация по сегодняшней дате
    today = timezone.now().date()
    apartments_today = apartments.filter(date=today)

    # Если нет данных за сегодня, фильтруем по вчерашней дате
    if not apartments_today.exists():
        yesterday = today - timedelta(days=1)
        apartments = apartments.filter(date=yesterday)
    else:
        apartments = apartments_today

    # Пагинация
    page = request.GET.get("page", 1)
    if page == "Next":
        page = 1
    else:
        page = int(page)
    apartments = apartments[(page - 1) * 9 : page * 9]

    # Подготовка параметров для передачи в шаблон
    current_page = int(request.GET.get("page", 1))
    next_page = current_page + 1

    # Составление параметров фильтров для сохранения при переходе между страницами
    filter_params = {
        "rooms": rooms,
        "min_size": min_size,
        "max_size": max_size,
        "order_by": order_by,
    }

    # Отправка данных в шаблон
    return render(
        request,
        "goods/catalog.html",
        {
            "apartments": apartments,
            "next_page": next_page,
            "page": page,
            "filter_params": filter_params,
        },
    )
