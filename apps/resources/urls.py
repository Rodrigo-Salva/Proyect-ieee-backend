from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EducationalResourceViewSet

router = DefaultRouter()
router.register(r'resources', EducationalResourceViewSet, basename='resource')

urlpatterns = [
    path('', include(router.urls)),
]