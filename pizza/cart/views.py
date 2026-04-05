from django.shortcuts import render

# Create your views here.
def cart_view(request):
    cart = request.session.get('cart', {})

    pizzas = []
    total = 0

    for pizza_id, quantity in cart.items():
        pizza = Pizza.objects.get(id=pizza_id)
        pizza.quantity = quantity
        pizza.total_price = pizza.price * quantity

        total += pizza.total_price
        pizzas.append(pizza)

    context = {
        'pizzas': pizzas,
        'total': total
    }

    return render(request, 'main/cart.html', context)