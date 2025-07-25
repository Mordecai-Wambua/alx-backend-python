from rest_framework import serializers
from .models import User, Message, Conversation


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "password",
            "phone_number",
            "role",
            "created_at",
        ]
        read_only_fields = ["user_id", "created_at"]

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            phone_number=validated_data.get("phone_number"),
            role=validated_data.get("role"),
        )
        user.set_password(validated_data["password"])  # 🔐 hash password
        user.save()
        return user


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "message_body",
            "sent_at",
        ]
        read_only_fields = ["message_id", "sent_at"]


class ConversationSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()
    participants = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all()
    )

    class Meta:
        model = Conversation
        fields = ("conversation_id", "participants", "messages", "created_at")
        read_only_fields = (
            "conversation_id",
            "created_at",
        )

    def get_messages(self, obj):
        return MessageSerializer(obj.messages.all(), many=True).data

    def validate(self, data):
        if not data.get("participants"):
            raise serializers.ValidationError(
                "Conversation must have at least one participant"
            )
        return data
