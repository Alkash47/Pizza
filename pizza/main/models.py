from django.db import models


class MenuItem(models.Model):
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=7, decimal_places=2)
    image = models.ImageField('Фото', upload_to='menu/', blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Dough(models.Model):
    title = models.CharField('Тесто', max_length=30)

    class Meta:
        verbose_name = 'Тесто'
        verbose_name_plural = 'Теста'

    def __str__(self):
        return self.title


class Toppings(models.Model):
    title = models.CharField('Название', max_length=30)
    slug = models.SlugField('Слаг', unique=True, max_length=64)

    class Meta:
        verbose_name = 'Добавка'
        verbose_name_plural = 'Добавки'

    def __str__(self):
        return self.title


class Pizza(MenuItem):
    toppings = models.ManyToManyField(Toppings, verbose_name='Топпинги')
    dough = models.ForeignKey(Dough, verbose_name='Тесто', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Пицца'
        verbose_name_plural = 'Пиццы'


class Snacks(MenuItem):
    class Meta:
        verbose_name = 'Закуска'
        verbose_name_plural = 'Закуски'


class Drinks(MenuItem):
    class Meta:
        verbose_name = 'Напиток'
        verbose_name_plural = 'Напитки'

class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = (
        (STATUS_NEW, 'New'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_CANCELLED, 'Cancelled'),
    )

    customer_name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=30)
    address = models.CharField('Адрес', max_length=255)
    comment = models.TextField('Комментарий к заказу', blank=True)
    total_price = models.DecimalField(
        'Стоимость заказа',
        max_digits=9,
        decimal_places=2,
        default=0,
    )
    status = models.CharField(
        'Статус заказа',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )
    created_at = models.DateTimeField('Заказ создан', auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ #{self.pk} - {self.customer_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
    )
    item_type = models.CharField('Item type', max_length=30)
    item_id = models.PositiveIntegerField('Item id')
    title = models.CharField('Title', max_length=100)
    quantity = models.PositiveIntegerField('Quantity')
    unit_price = models.DecimalField(
        'Unit price',
        max_digits=7,
        decimal_places=2,
    )
    total_price = models.DecimalField(
        'Total price',
        max_digits=9,
        decimal_places=2,
    )

    class Meta:
        verbose_name = 'Предмет заказа'
        verbose_name_plural = 'Предметы заказа'

    def __str__(self):
        return f'{self.title} x {self.quantity}'


class Desserts(MenuItem):
    class Meta:
        verbose_name = 'Десерт'
        verbose_name_plural = 'Десерты'
