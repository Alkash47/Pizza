from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from .models import Pizza, Snacks, Drinks, Desserts


MODEL_MAP = {
    'pizza': Pizza,
    'snacks': Snacks,
    'drinks': Drinks,
    'desserts': Desserts,
}


def index(request):
    context = {
        'pizzas': Pizza.objects.all(),
        'snacks': Snacks.objects.all(),
        'drinks': Drinks.objects.all(),
        'desserts': Desserts.objects.all(),
    }
    return render(request, 'main/index.html', context)


class PizzaDetailView(DetailView):
    model = Pizza
    template_name = 'main/pizza_detail.html'


def add_to_cart(request, item_type, item_id):
    cart = request.session.get('cart', {})

    item_type = item_type.lower()
    key = f'{item_type}_{item_id}'

    if key in cart:
        cart[key] += 1
    else:
        cart[key] = 1

    request.session['cart'] = cart
    return redirect('main:index')


def decrease_item(request, item_type, item_id):
    cart = request.session.get('cart', {})

    item_type = item_type.lower()
    key = f'{item_type}_{item_id}'

    if key in cart:
        cart[key] -= 1
        if cart[key] <= 0:
            del cart[key]

    request.session['cart'] = cart
    return redirect('main:cart')


def remove_from_cart(request, item_type, item_id):
    cart = request.session.get('cart', {})

    item_type = item_type.lower()
    key = f'{item_type}_{item_id}'

    if key in cart:
        del cart[key]

    request.session['cart'] = cart
    return redirect('main:cart')


def cart_view(request):
    cart = request.session.get('cart', {})

    items = []
    total = 0

    for key, quantity in cart.items():
        try:
            item_type, item_id = key.split('_')
            model = MODEL_MAP.get(item_type)

            if not model:
                continue

            item = model.objects.get(id=item_id)
            item.quantity = quantity
            item.total_price = item.price * quantity
            item.item_type = item_type

            total += item.total_price
            items.append(item)

        except (ValueError, model.DoesNotExist if 'model' in locals() and model else Exception):
            continue

    context = {
        'items': items,
        'total': total,
    }
    return render(request, 'main/cart.html', context)