from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only authenticated users to access the api
    Allow only participants in a conversation to send, view, update and delete messages
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        conversation = obj.conversation
        if request.method in permissions.SAFE_METHODS:
            return user in conversation.participants.all()
        if request.method in ['POST', 'PATCH', 'DELETE']:
            return user in conversation.participants.all()
        return False