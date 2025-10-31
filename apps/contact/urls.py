from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactFormViewSet, SocialLinkViewSet

router = DefaultRouter()
router.register(r'contact-forms', ContactFormViewSet, basename='contact-form')
router.register(r'social-links', SocialLinkViewSet, basename='social-link')

urlpatterns = [
    path('', include(router.urls)),
]