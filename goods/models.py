from django.db import models

class Flats(models.Model):
    flat_id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=20)
    price = models.IntegerField()
    apartment_size = models.FloatField()
    rooms = models.IntegerField()
    floor = models.IntegerField(null=True, blank=True)
    floor_max = models.IntegerField(null=True, blank=True)
    place = models.CharField(max_length=200)
    link = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.place} - {self.price} $"

    class Meta:
        db_table = "flats2"  # Соответствие имени таблицы в базе данных
