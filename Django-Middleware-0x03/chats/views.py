from rest_framework import viewsets, generics, status, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from .models import Conversation, Message
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import MessagePagination


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "user": UserSerializer(
                        user, context=self.get_serializer_context()
                    ).data,
                    "message": "User registered successfully.",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    queryset = Conversation.objects.all()

    def perform_create(self, serializer):
        participants_ids = self.request.data.get("participants", [])
        if not participants_ids:
            raise serializer.ValidationError("Participants field is required")
        conversation = serializer.save()
        conversation.participants.set(participants_ids)
        conversation.save()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = MessageFilter
    search_fields = ["message_body"]
    ordering_fields = ["sent_at"]
    ordering = ["-sent_at"]

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_pk")
        if not conversation_id:
            return Message.objects.none()
        try:
            # Check if the conversation exists first
            conversation = Conversation.objects.get(pk=conversation_id)
            if self.request.user not in conversation.participants.all():
                raise PermissionDenied("You are not a participant of this conversation")
            return Message.objects.filter(conversation=conversation)
        except Conversation.DoesNotExist:
            raise NotFound("Conversation not found")

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get("conversation_pk")
        if not conversation_id:
            raise NotFound(detail="Conversation ID is required.")

        try:
            conversation = Conversation.objects.get(pk=conversation_id)
        except Conversation.DoesNotExist:
            raise NotFound(detail="Conversation not found.")

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(
                detail="You are not a participant of this conversation",
                code=status.HTTP_403_FORBIDDEN,
            )
        serializer.save(sender=self.request.user, conversation=conversation)
