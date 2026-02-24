from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """Permiso personalizado solo para administradores"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """Administradores pueden editar, otros solo lectura"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and getattr(request.user, 'is_admin', False)


class IsOwnerOrAdmin(permissions.BasePermission):
    """Solo el propietario o admin pueden editar"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.is_admin
