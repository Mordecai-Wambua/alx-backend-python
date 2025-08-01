from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .serializers import (
    MessageSerializer,
    RegisterSerializer,
    RecursiveMessageSerializer,
)
from .models import Message


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user).select_related(
            "sender", "receiver", "edited_by", "parent_message"
        ).prefetch_related("replies")

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save(edited_by=self.request.user)
        instance.save()

    @action(detail=True, methods=["get"])
    def thread(self, request, pk=None):
        message = self.get_object()
        serializer = RecursiveMessageSerializer(message)
        return Response(serializer.data)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["delete"], url_path="user-delete")
    def delete_user(self, request):
        user = request.user
        user.delete()
        return Response(
            {"detail": "Account deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
