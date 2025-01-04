from goods.models import Flats
from django.db.models import Avg, Count


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
