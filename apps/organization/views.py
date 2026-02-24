from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Chapter, Branch, Member, Position
from .serializers import (
    ChapterSerializer, BranchSerializer, MemberSerializer, 
    MemberDetailSerializer, PositionSerializer
)
from apps.users.permissions import IsAdminOrReadOnly

class PositionViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar Cargos"""
    
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class ChapterViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar Capítulos"""
    
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Obtener miembros de un capítulo"""
        chapter = self.get_object()
        members = chapter.members.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)


class BranchViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar Ramas"""
    
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class MemberViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar Miembros"""
    
    queryset = Member.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['chapter', 'is_active', 'position']
    search_fields = ['full_name', 'email']
    ordering_fields = ['full_name', 'created_at']
    ordering = ['full_name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MemberDetailSerializer
        return MemberSerializer