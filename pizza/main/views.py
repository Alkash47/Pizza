from dataclasses import dataclass
from decimal import Decimal

from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView

from .forms import OrderForm
from .models import Desserts, Drinks, Order, OrderItem, Pizza, Snacks


MODEL_MAP = {
    'pizza': Pizza,
    'snacks': Snacks,
    'drinks': Drinks,
    'desserts': Desserts,
}

ITEM_TYPE_LABELS = {
    'pizza': 'Pizza',
    'snacks': 'Snack',
    'drinks': 'Drink',
    'desserts': 'Dessert',
}


@dataclass(frozen=True)
class CartItem:
    id: int
    item_type: str
    type_label: str
    title: str
    price: Decimal
    quantity: int
    total_price: Decimal


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


def _get_cart(session):
    return session.get('cart', {})


def _save_cart(session, cart):
    session['cart'] = cart
    session.modified = True


def _cart_key(item_type, item_id):
    return f'{item_type.lower()}_{item_id}'


def _get_cart_items(cart):
    grouped_ids = {}

    for key in cart:
        try:
            item_type, raw_item_id = key.split('_', maxsplit=1)
            item_id = int(raw_item_id)
        except (TypeError, ValueError):
            continue

        if item_type in MODEL_MAP:
            grouped_ids.setdefault(item_type, []).append(item_id)

    products = {}
    for item_type, ids in grouped_ids.items():
        products[item_type] = MODEL_MAP[item_type].objects.in_bulk(ids)

    items = []
    total = Decimal('0')

    for key, quantity in cart.items():
        try:
            item_type, raw_item_id = key.split('_', maxsplit=1)
            item_id = int(raw_item_id)
            quantity = int(quantity)
        except (TypeError, ValueError):
            continue

        if quantity <= 0:
            continue

        product = products.get(item_type, {}).get(item_id)
        if product is None:
            continue

        item_total = product.price * quantity
        total += item_total
        items.append(CartItem(
            id=product.id,
            item_type=item_type,
            type_label=ITEM_TYPE_LABELS.get(item_type, item_type),
            title=product.title,
            price=product.price,
            quantity=quantity,
            total_price=item_total,
        ))

    return items, total


def add_to_cart(request, item_type, item_id):
    if item_type not in MODEL_MAP:
        return redirect('main:index')

    get_object_or_404(MODEL_MAP[item_type], id=item_id)

    cart = _get_cart(request.session)
    key = _cart_key(item_type, item_id)
    cart[key] = cart.get(key, 0) + 1
    _save_cart(request.session, cart)
    return redirect(request.META.get('HTTP_REFERER', 'main:index'))


def decrease_item(request, item_type, item_id):
    cart = _get_cart(request.session)
    key = _cart_key(item_type, item_id)

    if key in cart:
        cart[key] -= 1
        if cart[key] <= 0:
            del cart[key]

    _save_cart(request.session, cart)
    return redirect('main:cart')


def remove_from_cart(request, item_type, item_id):
    cart = _get_cart(request.session)
    cart.pop(_cart_key(item_type, item_id), None)
    _save_cart(request.session, cart)
    return redirect('main:cart')


def cart_view(request):
    items, total = _get_cart_items(_get_cart(request.session))
    context = {
        'form': OrderForm(),
        'items': items,
        'total': total,
    }
    return render(request, 'main/cart.html', context)


def checkout(request):
    items, total = _get_cart_items(_get_cart(request.session))
    if not items:
        return redirect('main:cart')

    form = OrderForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        order = form.save(commit=False)
        order.total_price = total
        order.save()

        order_items = [
            OrderItem(
                order=order,
                item_type=item.item_type,
                item_id=item.id,
                title=item.title,
                quantity=item.quantity,
                unit_price=item.price,
                total_price=item.total_price,
            )
            for item in items
        ]
        OrderItem.objects.bulk_create(order_items)

        _save_cart(request.session, {})
        return redirect('main:order_success', order_id=order.id)

    context = {
        'form': form,
        'items': items,
        'total': total,
    }
    return render(request, 'main/checkout.html', context)


def order_success(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related('items'),
        id=order_id,
    )
    return render(request, 'main/order_success.html', {'order': order})
