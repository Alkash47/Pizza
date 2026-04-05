from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('pizzas/<int:pk>/', views.PizzaDetailView.as_view(), name='pizza_detail'),
    path('cart/', views.cart_view, name='cart'),

    path('add/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('decrease/<str:item_type>/<int:item_id>/', views.decrease_item, name='decrease_item'),
    path('remove/<str:item_type>/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]