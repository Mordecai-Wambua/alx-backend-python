from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from .models import Conversation, Message


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

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
    permission_classes = [permissions.AllowAny]

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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return conversations where current user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        # Auto-add current user as a participant when creating a conversation
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return messages in conversations the user participates in
        return Message.objects.filter(
            conversation_id__participants=self.request.user
        ).select_related("sender_id", "conversation_id")

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the sender
        message = serializer.save(sender_id=self.request.user)

        # Add user to conversation participants if not already
        conversation = message.conversation_id
        if self.request.user not in conversation.participants.all():
            conversation.participants.add(self.request.user)

