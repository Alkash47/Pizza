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

class Desserts(MenuItem):
    class Meta:
        verbose_name = 'Десерт'
        verbose_name_plural = 'Десерты'