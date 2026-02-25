from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.utils import timezone
from .models import News, Event, Announcement
from .serializers import NewsSerializer, NewsDetailSerializer, EventSerializer, AnnouncementSerializer
from apps.users.permissions import IsAdminOrReadOnly, IsOwnerOrAdmin

class NewsViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar Noticias"""
    
    serializer_class = NewsSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['is_published', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['published_date', 'created_at']
    ordering = ['-published_date']
    
    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_admin:
            return News.objects.all()
        return News.objects.filter(is_published=True)
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NewsDetailSerializer
        return NewsSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrReadOnly])
    def publish(self, request, pk=None):
        """Publicar noticia"""
        news = self.get_object()
        news.is_published = True
        news.published_date = timezone.now()
        news.save()
        serializer = self.get_serializer(news)
        return Response(serializer.data)


class EventViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar Eventos"""
    
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['location']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['event_date', 'created_at']
    ordering = ['-event_date']
    
    def get_queryset(self):
        return Event.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_interest(self, request, pk=None):
        """Alternar interés del usuario en un evento"""
        event = self.get_object()
        user = request.user
        
        if event.interested_users.filter(id=user.id).exists():
            event.interested_users.remove(user)
            message = "Ya no estás interesado en este evento"
            is_interested = False
        else:
            event.interested_users.add(user)
            message = "Ahora estás interesado en este evento"
            is_interested = True
            
        return Response({
            'detail': message,
            'is_interested': is_interested,
            'interested_count': event.interested_users.count()
        })


class AnnouncementViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar Convocatorias"""
    
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['deadline', 'created_at']
    ordering = ['-deadline']
    
    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_admin:
            return Announcement.objects.all()
        return Announcement.objects.filter(is_active=True)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener solo convocatorias activas"""
        active = Announcement.objects.filter(is_active=True).order_by('-deadline')
        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)