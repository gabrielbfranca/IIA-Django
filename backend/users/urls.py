from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationView, UserLoginView, UserProfileViewSet

router = DefaultRouter()
router.register(r"profile", UserProfileViewSet, basename="user-profile")

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("", include(router.urls)),
]
