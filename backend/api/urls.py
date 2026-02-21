from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import BookListViewSet, BookViewSet

router = DefaultRouter()
router.register(r"books", BookViewSet, basename="books")
router.register(r"lists", BookListViewSet, basename="lists")

urlpatterns = [
    path("", include(router.urls)),
]
