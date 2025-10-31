from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import EducationalResource
from .serializers import EducationalResourceSerializer
from apps.users.permissions import IsAdminOrReadOnly

class EducationalResourceViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar Recursos Educativos"""
    
    queryset = EducationalResource.objects.all()
    serializer_class = EducationalResourceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['category']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'download_count']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def download(self, request, pk=None):
        """Incrementar contador de descargas"""
        resource = self.get_object()
        resource.download_count += 1
        resource.save()
        serializer = self.get_serializer(resource)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def most_downloaded(self, request):
        """Obtener recursos más descargados"""
        resources = EducationalResource.objects.all().order_by('-download_count')[:10]
        serializer = self.get_serializer(resources, many=True)
        return Response(serializer.data)