from django.contrib import admin

from ads.models import Ad, Comment


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """
    Объявления - отображение в админ-панели Django.
    Фильтрует по названию товара.
    Поиск в названии товара и его описании.
    """
    list_display = ('pk', 'author', 'title', 'price', 'created_at')
    list_filter = ('title',)
    search_fields = ('title', 'description')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Отзывы - отображение в админ-панели Django.
    Фильтрует по автору.
    """
    list_display = ('pk', 'ad', 'author', 'text', 'created_at')
    list_filter = ('author',)
