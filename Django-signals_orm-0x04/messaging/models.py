import uuid
from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, related_name="received_messages", on_delete=models.CASCADE
    )
    content = models.TextField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="edited_messages",
        on_delete=models.SET_NULL,
    )
    parent_message = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    read = models.BooleanField(default=False)
    objects = models.Manager()
    unread = UnreadMessagesManager()

    def __str__(self):
        return f"{self.sender} to {self.receiver}"


class MessageHistory(models.Model):
    message_id = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="history"
    )
    content = models.TextField(null=False, blank=False)
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of: {self.message_id}"


class Notification(models.Model):
    notification_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message_id = models.ForeignKey(Message, on_delete=models.CASCADE)

    def __str__(self):
        return f"Notification for {self.user_id} - Message: {self.message_id}"
