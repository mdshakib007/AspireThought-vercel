from django.urls import path, include
from rest_framework import routers
from tag.views import TagViewSet, AddTagAPIView

router = routers.DefaultRouter()
router.register("list", TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("add/", AddTagAPIView.as_view(), name="add_tag"),
]
