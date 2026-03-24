from django.urls import path, include
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('pizzas/<int:pizza_id>/', views.pizza_detail, name='pizza_detail'),
]