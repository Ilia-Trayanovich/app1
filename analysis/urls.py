from django.urls import path

from analysis import views

app_name = "analysis"

urlpatterns = [
    path("<int:id>/", views.index, name="index"), 
]
