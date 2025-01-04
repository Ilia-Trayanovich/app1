from django.shortcuts import render
from .utils import get_graph_data
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import os

# Путь для сохранения графиков
GRAPH_DIR = '/static/analytics/graphs/'

def create_graph(x, y, title, xlabel, ylabel, filename):
    """Создает график и сохраняет его в файл"""
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    file_path = os.path.join(GRAPH_DIR, filename)
    plt.savefig(file_path, format='png')
    plt.close()
    return file_path

def create_histogram(data, title, xlabel, ylabel, filename):
    """Создает гистограмму и сохраняет её в файл"""
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=20, edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    file_path = os.path.join(GRAPH_DIR, filename)
    plt.savefig(file_path, format='png')
    plt.close()
    return file_path

def index(request):
    graph_data = get_graph_data()

    os.makedirs(GRAPH_DIR, exist_ok=True)
    
    # Генерация графиков
    graphs = [
        {
            "title": "График изменения средней стоимости квадратного метра по дням",
            "image": create_graph(
                graph_data['dates'], graph_data['avg_prices_per_sqm'],
                "Средняя цена за квадратный метр по дате", "Дата", "Цена за м²",
                "avg_price_per_sqm.png"
            )
        },
        {
            "title": "График изменения средней стоимости квартир по дням",
            "image": create_graph(
                graph_data['dates'], graph_data['avg_prices'],
                "Средняя стоимость квартир по дате", "Дата", "Цена квартиры",
                "avg_prices.png"
            )
        },
        {
            "title": "График изменения средней площади квартиры по дням",
            "image": create_graph(
                graph_data['dates'], graph_data['avg_sizes'],
                "Средняя площадь квартиры по дате", "Дата", "Площадь (м²)",
                "avg_sizes.png"
            )
        },
        {
            "title": "График распределения этажей по квартирам",
            "image": create_histogram(
                graph_data['floors'], "Распределение этажей квартир",
                "Этаж", "Частота", "floor_distribution.png"
            )
        },
        {
            "title": "Распределение стоимости квартир",
            "image": create_histogram(
                graph_data['prices'], "Распределение стоимости квартир",
                "Стоимость квартиры", "Частота", "price_distribution.png"
            )
        },
        {
            "title": "Распределение площади квартир",
            "image": create_histogram(
                graph_data['sizes'], "Распределение площади квартир",
                "Площадь квартиры (м²)", "Частота", "size_distribution.png"
            )
        },
        {
            "title": "График зависимости цены от площади",
            "image": create_graph(
                graph_data['sizes'], graph_data['prices'],
                "Зависимость цены от площади", "Площадь (м²)", "Цена квартиры",
                "price_vs_size.png"
            )
        },
        {
            "title": "График зависимости цены от этажа",
            "image": create_graph(
                graph_data['floors'], graph_data['prices'],
                "Зависимость цены от этажа", "Этаж", "Цена квартиры",
                "price_vs_floor.png"
            )
        },
        {
            "title": "График числа квартир по дням",
            "image": create_graph(
                graph_data['dates'], graph_data['num_flats'],
                "Число квартир по дням", "Дата", "Количество квартир",
                "num_flats_per_day.png"
            )
        }
    ]

    return render(request, 'analytics/index.html', {
        'content': 'Аналитика данных о квартирах',
        'graphs': graphs
    })
