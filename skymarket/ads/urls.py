from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from ads.apps import SalesConfig
from ads.views import AdViewSet, CommentViewSet, MyAdListAPIView

ads_router = SimpleRouter()
ads_router.register("ads", AdViewSet, basename='ads')

comment_router = NestedSimpleRouter(ads_router, 'ads', lookup='ad')
comment_router.register("comments", CommentViewSet, basename='comments')
app_name = SalesConfig.name

urlpatterns = [
    path("", include(ads_router.urls)),
    path("ad/me/", MyAdListAPIView.as_view(), name='user_ads'),
    path("", include(comment_router.urls)),
]
