from django.urls import path

from parser import views

app_name = "parser"

urlpatterns = [
    path('run/', views.run_parser_view, name='run'),
    ]