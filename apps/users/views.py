from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer, UserDetailSerializer, UserCreateSerializer,
    RegisterSerializer, CustomTokenObtainPairSerializer
)
from .permissions import IsAdminUser

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    """Vista personalizada para obtener tokens"""
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    """Vista para registro de nuevos usuarios"""
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generar tokens para el usuario recién registrado
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar usuarios"""
    
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        if self.action in ['list', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        """Obtener o actualizar el perfil del usuario autenticado"""
        if request.method in ['PUT', 'PATCH']:
            serializer = UserDetailSerializer(request.user, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserDetailSerializer(request.user, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def dashboard(self, request):
        """Panel principal con eventos, recursos y estado de membresía"""
        user = request.user
        
        # 1. Estado de membresía
        from apps.organization.models import Member
        is_official = Member.objects.filter(email=user.email).exists()
        membership_status = "Miembro Oficial" if is_official else "Usuario Público"
        
        # 2. Eventos próximos (3 más cercanos)
        from django.utils import timezone
        from apps.content.models import Event
        upcoming_events = Event.objects.filter(
            event_date__gte=timezone.now()
        ).order_by('event_date')[:3]
        
        # 3. Recursos recomendados (basados en capítulos de interés)
        from apps.resources.models import EducationalResource
        interested_chapter_ids = user.interested_chapters.values_list('id', flat=True)
        
        if interested_chapter_ids:
            recommended_resources = EducationalResource.objects.filter(
                chapter_id__in=interested_chapter_ids
            ).order_by('-download_count')[:3]
        else:
            recommended_resources = EducationalResource.objects.order_by('-download_count')[:3]
        
        # Formatear data para el frontend
        from apps.content.serializers import EventSerializer # Necesito verificar si existe
        from apps.resources.serializers import EducationalResourceSerializer # Necesito verificar si existe
        
        # Formatear data para el frontend con URLs absolutas
        data = {
            'membership_status': membership_status,
            'is_official_member': is_official,
            'upcoming_events': [{
                'id': e.id,
                'title': e.title,
                'description': e.description,
                'date': e.event_date,
                'location': e.location,
                'image_url': request.build_absolute_uri(e.image.url) if e.image else None,
                'interest_count': e.interested_users.count(),
                'is_interested': e.interested_users.filter(id=user.id).exists()
            } for e in upcoming_events],
            'recommended_resources': [{
                'id': r.id,
                'title': r.title,
                'description': r.description,
                'file_url': request.build_absolute_uri(r.file.url) if r.file else None,
                'downloads': r.download_count,
                'category': r.get_category_display()
            } for r in recommended_resources]
        }
        
        return Response(data)

    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def activate_user(self, request):
        """Activar usuario (solo admin)"""
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            return Response({'status': 'Usuario activado'})
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
