from django.conf import settings
from django.db import models


class Ad(models.Model):
    title = models.CharField(max_length=150, verbose_name='название товара')
    price = models. IntegerField(verbose_name='цена товара')
    description = models.TextField(verbose_name='описание товара')
    image = models.ImageField(upload_to='ads/', null=True, blank=True, verbose_name='Изображение')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='автор объявления')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='создан')

    def str(self):
        return f'{self.title} {self.price}'

    class Meta:
        verbose_name = 'объявление'
        verbose_name_plural = 'объявления'
        ordering = ('-created_at',)


class Comment(models.Model):
    text = models.TextField(verbose_name='текст отзыва')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='автор отзыва')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name='объявление')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='создан')

    def str(self):
        return f'{self.author} от {self.created_at}'

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
