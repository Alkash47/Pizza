from django.db import models

# Create your models here.
class Pizza(models.Model):
    title = models.CharField(verbose_name='Название', max_length=100)
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(verbose_name='Цена', max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = 'Пицца'
        verbose_name_plural = 'Пиццы'
