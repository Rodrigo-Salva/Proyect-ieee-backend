from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer básico para usuario con URL absoluta para avatar"""
    
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'role', 'avatar', 'avatar_url', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_avatar_url(self, obj):
        if not obj.avatar:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.avatar.url)
        return obj.avatar.url


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para usuario con URL absoluta para avatar"""
    
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 
            'role', 'is_active', 'phone', 'biography', 'ieee_id', 
            'avatar', 'avatar_url', 'interested_chapters', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_avatar_url(self, obj):
        if not obj.avatar:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.avatar.url)
        return obj.avatar.url


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
    """Serializer personalizado para obtener tokens con soporte para email/username"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Permitimos que el campo se llame 'email' o 'username'
        self.fields['email'] = serializers.EmailField(required=False)
        self.fields['username'] = serializers.CharField(required=False)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['role'] = user.role
        return token
    
    def validate(self, attrs):
        # Intentamos obtener el identificador de 'email' o 'username'
        identifier = attrs.get('email') or attrs.get('username')
        password = attrs.get('password')

        if not identifier:
            raise serializers.ValidationError({'detail': 'Debe proporcionar un email o username'})

        # Importación diferida para evitar ciclos
        from django.contrib.auth import authenticate
        
        # Intentamos autenticar (Django usará el email si USERNAME_FIELD='email')
        user = authenticate(email=identifier, password=password)

        if not user:
            # Reintento por si el backend espera el kwarg 'username'
            user = authenticate(username=identifier, password=password)

        if user:
            if not user.is_active:
                raise serializers.ValidationError({'detail': 'Esta cuenta está desactivada'})
            
            self.user = user
            refresh = self.get_token(self.user)

            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(self.user, context=self.context).data
            }
            return data

        raise serializers.ValidationError({'detail': 'No se encontró ninguna cuenta activa con las credenciales proporcionadas'})