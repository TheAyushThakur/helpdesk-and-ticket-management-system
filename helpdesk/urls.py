from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, RegisterView, LoginView, LogoutView, CommentViewSet

router= DefaultRouter()
router.register('tickets', TicketViewSet)
router.register(r'comments', CommentViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
