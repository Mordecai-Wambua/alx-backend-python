from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user in obj.conversation.participants.all()
        # return obj.conversation.filter(id=request.user.id).exists()