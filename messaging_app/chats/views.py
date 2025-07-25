from rest_framework import viewsets, generics, status, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate
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


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)

            response = Response({
                "user": {
                    "id": user.user_id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
            })

            # Set token as HTTP-only cookie
            response.set_cookie(
                key='auth_token',
                value=token.key,
                httponly=True,  # prevents JavaScript access (XSS protection)
                secure=False,  # set to True in production (HTTPS)
                samesite='Lax'  # or 'Strict'/'None' depending on your frontend
            )
            return response

        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Only return conversations where user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        participants_ids = self.request.data.get('participants', [])
        if not participants_ids:
            raise serializer.ValidationError("Participants field is required")
        conversation = serializer.save()
        conversation.participants.set(participants_ids)
        conversation.save()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ["message_body"]
    ordering_fields = ["sent_at"]
    ordering = ["-sent_at"]

    def get_queryset(self):
        conversation_pk = self.kwargs["conversation_pk"]
        return Message.objects.filter(conversation__pk=conversation_pk, conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation_pk = self.kwargs["conversation_pk"]
        conversation = Conversation.objects.get(pk=conversation_pk)
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(detail="You are not a participant of this conversation", code=status.HTTP_403_FORBIDDEN)
        serializer.save(sender=self.request.user, conversation=conversation)


