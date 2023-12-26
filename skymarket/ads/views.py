from rest_framework import pagination, viewsets, generics
from rest_framework.decorators import action
from ads.models import Ad, Comment
from ads.serializers import AdSerializer, CommentSerializer, AdDetailSerializer


class AdPagination(pagination.PageNumberPagination):
    pass


class AdViewSet(viewsets.ModelViewSet):
    serializer_class = AdDetailSerializer
    queryset = Ad.objects.all()

    # def get_queryset(self):
    #     pk = self.kwargs.get('pk')
    #     if not pk:
    #         return Ad.objects.all()
    #
    #     return Ad.objects.filter(pk=pk)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class MyAdListAPIView(generics.ListAPIView):
    serializer_class = AdDetailSerializer
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

