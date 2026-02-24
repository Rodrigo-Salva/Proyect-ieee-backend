from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer básico para usuario"""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'role', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear nuevo usuario (Admin)"""
    
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'role']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer para registro de usuarios públicos"""
    
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password_confirm']
    
    def validate(self, data):
        if data['password'] != data.get('password_confirm'):
            raise serializers.ValidationError({'password': 'Las contraseñas no coinciden'})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        # Por defecto el rol es 'public' según el modelo
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer personalizado para obtener tokens con info de usuario"""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['role'] = user.role
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data