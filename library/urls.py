from rest_framework.routers import DefaultRouter

from .views import AuthorViewSet, BookViewSet, BorrowViewSet

app_name = "library"
router = DefaultRouter()


router.register("books", BookViewSet, "book")
router.register("authors", AuthorViewSet, "author")
router.register("borrows", BorrowViewSet, "borrow")

urlpatterns = [] + router.urls
