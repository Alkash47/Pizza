from django.shortcuts import render
from .models import Pizza
# Create your views here.

def index(request):
    template_name = 'main/index.html'
    pizza_list = Pizza.objects.all()
    context = {'pizza_list': pizza_list}
    return render(request, template_name, context)

def pizza_detail(request, pizza_id):
    pass
