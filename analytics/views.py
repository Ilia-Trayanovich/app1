from django.shortcuts import render


def index(request):
    graphs = (
        {
            "image": "avg_price_per_sqm.png",
            "title": "График изменения средней стоимости квадратного метра по дням",
        },
        {
            "image": "avg_prices.png",
            "title": "График изменения средней стоимости квартир по дням",
        },
        {
            "image": "avg_sizes.png",
            "title": "График изменения средней площади квартиры по дням",
        },
        {
            "image": "floor_distribution.png",
            "title": "График распределения этажей по квартирам",
        },
        {"image": "price_distribution.png", "title": "Распределение стоимости квартир"},
        {"image": "price_vs_floor.png", "title": "График зависимости цены от этажа"},
        {"image": "num_flats_per_day.png", "title": "График числа квартир по дням"},
    )

    return render(
        request,
        "analytics/index.html",
        {"content": "Аналитика данных о квартирах", "graphs": graphs},
    )
