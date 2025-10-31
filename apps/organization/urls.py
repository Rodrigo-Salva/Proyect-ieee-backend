from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChapterViewSet, BranchViewSet, MemberViewSet

router = DefaultRouter()
router.register(r'chapters', ChapterViewSet, basename='chapter')
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'members', MemberViewSet, basename='member')

urlpatterns = [
    path('', include(router.urls)),
]