from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from .models import Conversation


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only authenticated users to access the api
    Allow only participants in a conversation to send, view, update and delete messages
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        # Check conversation access for nested routes
        conversation_pk = view.kwargs.get("conversation_pk")
        if conversation_pk:
            try:
                conversation = Conversation.objects.get(pk=conversation_pk)
                if request.method in ["POST", "PATCH", "PUT", "DELETE"]:
                    return request.user in conversation.participants.all()
                return True  # Allow GET requests, object-level permission will filter
            except Conversation.DoesNotExist:
                return False
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        # Handle both Message and Conversation objects
        conversation = obj if hasattr(obj, "participants") else obj.conversation

        if user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant of this conversation")

        if request.method in ["POST", "PATCH", "PUT", "DELETE"]:
            return user in conversation.participants.all()
        return True
