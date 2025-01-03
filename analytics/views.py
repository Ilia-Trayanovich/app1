from django.shortcuts import render
from .utils import get_graph_data
import matplotlib
matplotlib.use('Agg')  # Использование бэкенда для серверной отрисовки
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def create_graph(x, y, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"

def create_histogram(data, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=20, edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"

def index(request):
    graph_data = get_graph_data()
    
    # Генерация графиков
    graphs = [
        {
            "title": "График изменения средней стоимости квадратного метра по дням",
            "image": create_graph(
                graph_data['dates'], graph_data['avg_prices_per_sqm'],
                "Средняя цена за квадратный метр по дате", "Дата", "Цена за м²"
            )
        },
        {
            "title": "График изменения средней стоимости квартир по дням",
            "image": create_graph(
                graph_data['dates'], graph_data['avg_prices'],
                "Средняя стоимость квартир по дате", "Дата", "Цена квартиры"
            )
        },
        {
            "title": "График изменения средней площади квартиры по дням",
            "image": create_graph(
                graph_data['dates'], graph_data['avg_sizes'],
                "Средняя площадь квартиры по дате", "Дата", "Площадь (м²)"
            )
        },
                {
            "title": "График распределения этажей квартир",
            "image": create_histogram(
                graph_data['floors'], "Распределение этажей квартир",
                "Этаж", "Частота"
            )
        },
        {
            "title": "Распределение стоимости квартир                      |",
            "image": create_histogram(
                graph_data['prices'], "Распределение стоимости квартир",
                "Стоимость квартиры", "Частота"
            )
        },
        {
            "title": "Распределение площади квартир",
            "image": create_histogram(
                graph_data['sizes'], "Распределение площади квартир",
                "Площадь квартиры (м²)", "Частота"
            )
        },
        {
            "title": "График зависимости цены от площади",
            "image": create_graph(
                graph_data['sizes'], graph_data['prices'],
                "Зависимость цены от площади", "Площадь (м²)", "Цена квартиры"
            )
        },
        {
            "title": "График зависимости цены от этажа",
            "image": create_graph(
                graph_data['floors'], graph_data['prices'],
                "Зависимость цены от этажа", "Этаж", "Цена квартиры"
            )
        },

        {
            "title": "График числа квартир по дням",
            "image": create_graph(
                graph_data['dates'], graph_data['num_flats'],
                "Число квартир по дням", "Дата", "Количество квартир"
            )
        }
    ]

    return render(request, 'analytics/index.html', {
        'content': 'Аналитика данных о квартирах',
        'graphs': graphs
    })
