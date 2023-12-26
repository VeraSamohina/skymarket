from django.urls import include, path
from rest_framework.routers import SimpleRouter

from ads.apps import SalesConfig
from ads.views import AdViewSet, CommentViewSet, MyAdListAPIView

ads_router = SimpleRouter()
ads_router.register("ads", AdViewSet)

comment_router = SimpleRouter()
comment_router.register("comments", CommentViewSet, basename='comments')
app_name = SalesConfig.name

urlpatterns = [
    path("", include(ads_router.urls)),
    path("ad/me/", MyAdListAPIView.as_view(), name='user_ads'),
    path("comments/", include(comment_router.urls)),
]
