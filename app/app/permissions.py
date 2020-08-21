from rest_framework import permissions


class IsOwnerOrAdminUser(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True
        if request.user.pk == request.parser_context['kwargs']['pk']:
            return True
