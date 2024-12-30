from django.shortcuts import render
from django.template import context

from .models import Flats

def catalog(request):
    # Начальные параметры фильтрации
    apartments = Flats.objects.all()
    
    # Фильтрация по количеству комнат
    rooms = request.GET.get('rooms')
    if rooms:
        apartments = apartments.filter(rooms=rooms)

    # Фильтрация по размеру квартиры
    min_size = request.GET.get('min_size')
    max_size = request.GET.get('max_size')
    if min_size:
        apartments = apartments.filter(apartment_size__gte=min_size)
    if max_size:
        apartments = apartments.filter(apartment_size__lte=max_size)
    
    # Сортировка по цене
    order_by = request.GET.get('order_by', 'default')
    if order_by == 'price':
        apartments = apartments.order_by('price')
    elif order_by == '-price':
        apartments = apartments.order_by('-price')

    # Пагинация
    page = request.GET.get('page', 1)
    apartments = apartments[(int(page)-1)*9:int(page)*9]

    # Отправка данных в шаблон
    return render(request, 'goods/catalog.html', {'apartments': apartments})
