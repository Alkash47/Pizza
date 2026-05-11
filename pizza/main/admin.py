from django.contrib import admin

from .models import (
    Desserts,
    Dough,
    Drinks,
    Order,
    OrderItem,
    Pizza,
    Snacks,
    Toppings,
)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'title',
        'item_type',
        'quantity',
        'unit_price',
        'total_price',
    )
    list_filter = ('item_type',)
    search_fields = ('title', 'order__customer_name', 'order__phone')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        'item_type',
        'item_id',
        'title',
        'quantity',
        'unit_price',
        'total_price',
    )
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer_name',
        'phone',
        'total_price',
        'status',
        'created_at',
    )
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'phone', 'address')
    inlines = (OrderItemInline,)


admin.site.register(Pizza)
admin.site.register(Toppings)
admin.site.register(Dough)
admin.site.register(Snacks)
admin.site.register(Drinks)
admin.site.register(Desserts)
