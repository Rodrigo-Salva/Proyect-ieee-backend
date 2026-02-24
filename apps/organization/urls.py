from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChapterViewSet, BranchViewSet, MemberViewSet, PositionViewSet

router = DefaultRouter()
router.register(r'chapters', ChapterViewSet, basename='chapter')
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'members', MemberViewSet, basename='member')
router.register(r'positions', PositionViewSet, basename='position')

urlpatterns = [
    path('', include(router.urls)),
]