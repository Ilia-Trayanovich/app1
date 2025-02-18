from goods.models import Flats
from django.db.models import Avg, Count
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os


def get_graph_data():

    grouped_data = (
        Flats.objects.exclude(price=None, apartment_size=None)
        .values("date")
        .annotate(
            avg_price_per_sqm=Avg("price") / Avg("apartment_size"),
            avg_price=Avg("price"),
            avg_size=Avg("apartment_size"),
            num_flats=Count("flat_id"),
        )
        .order_by("date")
    )

    all_prices = Flats.objects.exclude(price=None).values_list("price", flat=True)
    all_sizes = Flats.objects.exclude(apartment_size=None).values_list(
        "apartment_size", flat=True
    )
    all_floors = Flats.objects.exclude(floor=None).values_list("floor", flat=True)

    print(len(all_prices), len(all_sizes), len(all_floors))

    graph_data = {
        "dates": [entry["date"] for entry in grouped_data],
        "avg_prices_per_sqm": [entry["avg_price_per_sqm"] for entry in grouped_data],
        "avg_prices": [entry["avg_price"] for entry in grouped_data],
        "avg_sizes": [entry["avg_size"] for entry in grouped_data],
        "num_flats": [entry["num_flats"] for entry in grouped_data],
        "prices": list(all_prices),
        "sizes": list(all_sizes),
        "floors": [floor for floor in all_floors if floor is not None],
    }

    min_length = min(
        len(graph_data["sizes"]), len(graph_data["prices"]), len(graph_data["floors"])
    )
    graph_data["sizes"] = graph_data["sizes"][:min_length]
    graph_data["prices"] = graph_data["prices"][:min_length]
    graph_data["floors"] = graph_data["floors"][:min_length]

    return graph_data


GRAPH_DIR = "static/analytics/graphs/"  # Путь для сохранения графиков


def create_graph(x, y, title, xlabel, ylabel, filename):

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker="o")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    file_path = os.path.join(GRAPH_DIR, filename)
    plt.savefig(file_path, format="png")
    plt.close()
    return file_path


def create_histogram(data, title, xlabel, ylabel, filename):

    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=20, edgecolor="black")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    file_path = os.path.join(GRAPH_DIR, filename)
    plt.savefig(file_path, format="png")
    plt.close()
    return file_path


def generate_graphs():

    graph_data = get_graph_data()

    os.makedirs(GRAPH_DIR, exist_ok=True)

    # Генерация графиков
    graphs = [
        {
            "title": "График изменения средней стоимости квадратного метра по дням",
            "image": create_graph(
                graph_data["dates"],
                graph_data["avg_prices_per_sqm"],
                "Средняя цена за квадратный метр по дате",
                "Дата",
                "Цена за м²",
                "avg_price_per_sqm.png",
            ),
        },
        {
            "title": "График изменения средней стоимости квартир по дням",
            "image": create_graph(
                graph_data["dates"],
                graph_data["avg_prices"],
                "Средняя стоимость квартир по дате",
                "Дата",
                "Цена квартиры",
                "avg_prices.png",
            ),
        },
        {
            "title": "График изменения средней площади квартиры по дням",
            "image": create_graph(
                graph_data["dates"],
                graph_data["avg_sizes"],
                "Средняя площадь квартиры по дате",
                "Дата",
                "Площадь (м²)",
                "avg_sizes.png",
            ),
        },
        {
            "title": "График распределения этажей по квартирам",
            "image": create_histogram(
                graph_data["floors"],
                "Распределение этажей квартир",
                "Этаж",
                "Частота",
                "floor_distribution.png",
            ),
        },
        {
            "title": "Распределение стоимости квартир",
            "image": create_histogram(
                graph_data["prices"],
                "Распределение стоимости квартир",
                "Стоимость квартиры",
                "Частота",
                "price_distribution.png",
            ),
        },
        {
            "title": "Распределение площади квартир",
            "image": create_histogram(
                graph_data["sizes"],
                "Распределение площади квартир",
                "Площадь квартиры (м²)",
                "Частота",
                "size_distribution.png",
            ),
        },
        {
            "title": "График зависимости цены от площади",
            "image": create_graph(
                graph_data["sizes"],
                graph_data["prices"],
                "Зависимость цены от площади",
                "Площадь (м²)",
                "Цена квартиры",
                "price_vs_size.png",
            ),
        },
        {
            "title": "График зависимости цены от этажа",
            "image": create_graph(
                graph_data["floors"],
                graph_data["prices"],
                "Зависимость цены от этажа",
                "Этаж",
                "Цена квартиры",
                "price_vs_floor.png",
            ),
        },
        {
            "title": "График числа квартир по дням",
            "image": create_graph(
                graph_data["dates"],
                graph_data["num_flats"],
                "Число квартир по дням",
                "Дата",
                "Количество квартир",
                "num_flats_per_day.png",
            ),
        },
    ]

    return graphs
