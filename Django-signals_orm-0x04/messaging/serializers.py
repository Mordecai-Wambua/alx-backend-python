from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message, Notification


class RecursiveMessageSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "receiver",
            "content",
            "timestamp",
            "edited",
            "edited_by",
            "parent_message",
            "replies",
        ]

    def get_replies(self, obj):
        serializer = RecursiveMessageSerializer(obj.replies.all(), many=True)
        return serializer.data


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source="sender.username")
    receiver = serializers.ReadOnlyField(source="receiver.username")
    edited_by = serializers.ReadOnlyField(source="edited_by.username")
    replies = RecursiveMessageSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
