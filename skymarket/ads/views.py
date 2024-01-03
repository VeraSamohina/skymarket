from rest_framework import pagination, viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from ads.models import Ad, Comment
from ads.permissions import IsOwner, IsAdmin
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
    """
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter
    pagination_class = AdPagination
    queryset = Ad.objects.all()

    def get_permissions(self):
        """
        Установление прав доступа.
        Неавторизированный пользователь может видеть список объявлений.

        Авторизированный пользователь может:
        - видеть список объявлений;
        - видеть одно объявление (детально);
        - создавать объявления;
        - редактировать и удалять свои объявления.

        Администратор дополнительно к правам авторизованного пользователя может редактировать и удалять чужие объявления

        """

        if self.action in ['retrieve', 'create']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwner | IsAdmin]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Выбор сериализатора зависит от self.action.
        """

        if self.action in ['list', 'create']:
            return AdSerializer
        return AdDetailSerializer

    def perform_create(self, serializer):
        """
            Создание нового объявление и установление автора.
        """
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
        Вьюсет для модели Отзывов (Comment) к объявлениям
    """
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_permissions(self):
        """
        Определяет права доступа в зависимости от выполняемого действия.
        """
        if self.action in ['retrieve', 'create']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwner | IsAdmin]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """
        Создание комментария и установление автора.
        """
        ad_id = self.kwargs['ad_id']
        serializer.save(author=self.request.user, ad=Ad.objects.get(pk=ad_id))

    def perform_update(self, serializer):
        ad_id = self.kwargs['ad_id']
        serializer.save(author=self.request.user, ad=Ad.objects.get(pk=ad_id))

    def get_queryset(self):
        return self.queryset.filter(ad=self.kwargs['ad_pk']).select_related("author")
