import base64
import io
import matplotlib.pyplot as plt
from django.shortcuts import render, get_object_or_404
from goods.models import Flats
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np

def index(request, id):
    # Получаем данные для конкретной квартиры по id, если квартира не найдена, возвращаем ошибку 404
    apartment = get_object_or_404(Flats, flat_id=id)
    apartments = Flats.objects.all()

    # 1. Сравнение стоимости квартиры с аналогичными
    x_values = [a.apartment_size for a in apartments]  # Площадь всех квартир
    y_values = [a.price for a in apartments]  # Стоимость всех квартир

    # Выделяем выбранную квартиру
    colors = ['red' if a.flat_id == apartment.flat_id else 'blue' for a in apartments]

    # Строим график для сравнения стоимости квартиры с аналогичными
    fig, ax = plt.subplots()
    scatter = ax.scatter(x_values, y_values, c=colors, label='Квартиры')

    # Находим индекс выбранной квартиры в списке
    selected_apartment_idx = next((i for i, a in enumerate(apartments) if a.flat_id == apartment.flat_id), None)

    # Если выбрана квартира, то выделяем её красной точкой
    if selected_apartment_idx is not None:
        ax.scatter(x_values[selected_apartment_idx], y_values[selected_apartment_idx], c='red', label='Ваша квартира', edgecolors='black', s=100, zorder=5)

    ax.set_xlabel('Площадь квартиры')
    ax.set_ylabel('Стоимость квартиры')
    ax.set_title('Сравнение стоимости квартиры с аналогичными предложениями')
    ax.legend()

    # Сохраняем изображение в памяти
    img_stream = io.BytesIO()
    FigureCanvas(fig).print_png(img_stream)
    img_stream.seek(0)
    graph1_image = base64.b64encode(img_stream.getvalue()).decode('utf-8')
    graph1_image_data_uri = f"data:image/png;base64,{graph1_image}"

    # 2. Рейтинг квартиры по стоимости на квадратный метр
    price_per_m2 = [a.price / a.apartment_size for a in apartments if a.apartment_size > 0]
    sorted_apartments = sorted(zip(apartments, price_per_m2), key=lambda x: x[1])
    ratings = [x[1] for x in sorted_apartments]
    apartment_rating = next((i for i, x in enumerate(sorted_apartments) if x[0] == apartment), -1)

    # Строим график для рейтинга
    fig, ax = plt.subplots()
    ax.plot(range(len(ratings)), ratings, label='Рейтинг по стоимости м2')
    ax.scatter(apartment_rating, ratings[apartment_rating], color='red', label='Ваша квартира')
    ax.set_xlabel('Позиция квартиры')
    ax.set_ylabel('Стоимость за м2')
    ax.set_title('Рейтинг квартиры по стоимости на квадратный метр')
    ax.legend()

    # Сохраняем изображение в памяти
    img_stream = io.BytesIO()
    FigureCanvas(fig).print_png(img_stream)
    img_stream.seek(0)
    graph2_image = base64.b64encode(img_stream.getvalue()).decode('utf-8')
    graph2_image_data_uri = f"data:image/png;base64,{graph2_image}"

     # 3. Позиционирование квартиры в процентильном разрезе
    prices = [a.price for a in apartments]
    sizes = [a.apartment_size for a in apartments]

    # Вычисление процентилей для цен и площади
    price_percentile = np.percentile(prices, 50)  # Средний процентиль цены
    size_percentile = np.percentile(sizes, 50)  # Средний процентиль площади
    
    # Нормализуем данные для построения графика
    price_percentiles = [100 * (p / price_percentile) for p in prices]
    size_percentiles = [100 * (s / size_percentile) for s in sizes]

    # Строим график для позиционирования
    fig, ax = plt.subplots()
    ax.plot(prices, price_percentiles, label='Цена в процентилях')
    ax.plot(sizes, size_percentiles, label='Площадь в процентилях')
    ax.scatter(apartment.price, 100 * (apartment.price / price_percentile), color='red', label='Ваша квартира по цене')
    ax.scatter(apartment.apartment_size, 100 * (apartment.apartment_size / size_percentile), color='blue', label='Ваша квартира по площади')
    ax.set_xlabel('Цена / Площадь')
    ax.set_ylabel('Процентиль')
    ax.set_title('Позиционирование квартиры в процентильном разрезе')
    ax.legend()

    # Сохраняем изображение в памяти
    img_stream = io.BytesIO()
    FigureCanvas(fig).print_png(img_stream)
    img_stream.seek(0)
    graph3_image = base64.b64encode(img_stream.getvalue()).decode('utf-8')
    graph3_image_data_uri = f"data:image/png;base64,{graph3_image}"

    # Передаем данные в контекст
    context = {
        "title": "Home - Главная",
        "content": "Анализ квартиры",
        "apartment_id": id,
        "graphs": [
            {"title": "Сравнение стоимости квартиры с аналогичными", "image": graph1_image_data_uri},
            {"title": "Рейтинг квартиры по стоимости на квадратный метр", "image": graph2_image_data_uri},
            {"title": "Позиционирование квартиры в процентильном разрезе", "image": graph3_image_data_uri},
        ]
    }

    return render(request, "analysis/index.html", context)


       