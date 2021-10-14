from django.urls import path, include

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from . import views


router = DefaultRouter()
router.register('users', views.UserViewSet)

auth_views = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = [
    path('representatives/', views.RepresentativeAPIView.as_view(), name='representatives'),
    path('representatives/<int:pk>/', views.RepresentativeAPIView.as_view(), name='representative'),
    path('people/', views.HumansAPIView.as_view()),
    path('', include(router.urls)),
    path('', include(auth_views)),
    path('create_user/', views.UserCreateAPIView.as_view(), name="custom_create_user")
]