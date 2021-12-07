from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest import views

router = DefaultRouter()
router.register(r'user-object', views.UserObjectViewSet, basename='user-object')

urlpatterns = [
    path('', include(router.urls)),
]
