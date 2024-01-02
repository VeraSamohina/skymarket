from rest_framework import pagination, viewsets, generics
from ads.models import Ad, Comment
from ads.serializers import AdSerializer, CommentSerializer, AdDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend
from ads.filters import AdFilter


class AdPagination(pagination.PageNumberPagination):
    """
        Класс пагинации для списка объявлений.
    """
    page_size = 4


class AdViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели Объявление (Ad).
    Используется созданный фильтр по названию и пагинация.
    При создании поле "автор" заполняется текущим пользователем
    """
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter
    pagination_class = AdPagination
    queryset = Ad.objects.all()

    def get_serializer_class(self):
        """
        Выбор сериализатора зависит от self.action.
        """

        if self.action in ['list']:
            return AdSerializer
        return AdDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class MyAdListAPIView(generics.ListAPIView):
    """
    Класс представление для вывода списка объявлений текущего пользователя
    """
    serializer_class = AdSerializer
    queryset = Ad.objects.all()
    pagination_class = AdPagination

    def list(self, request, *args, **kwargs):
        """
        Список всех объявлений текущего пользователя.
        """
        self.queryset = self.queryset.filter(author=request.user)
        return super().list(request, *args, *kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    """
        Вьюсет для модели Отзывов (Comment)
    """
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        """
        Создание комментария и установление автора.
        """
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(ad=self.kwargs['ad_pk']).select_related("author")
