from rest_framework import pagination, viewsets, generics
from ads.models import Ad, Comment
from ads.serializers import AdSerializer, CommentSerializer, AdDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend
from ads.filters import AdFilter


class AdPagination(pagination.PageNumberPagination):
    pass


class AdViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter
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
    serializer_class = AdSerializer
    queryset = Ad.objects.all()

    def list(self, request, *args, **kwargs):
        """
        Список всех объявлений выбранного пользователя.
        """
        self.queryset = self.queryset.filter(author=request.user)
        return super().list(request, *args, *kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

