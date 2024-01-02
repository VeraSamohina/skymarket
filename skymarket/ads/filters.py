import django_filters
from ads.models import Ad


class AdFilter(django_filters.rest_framework.FilterSet):
    """
    Фильтр для модели Объявление, фильтрация происходит по полю 'title'
    """
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains", )

    class Meta:
        model = Ad
        fields = ("title",)
