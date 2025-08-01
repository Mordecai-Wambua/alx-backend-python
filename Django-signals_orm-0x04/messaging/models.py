from django.db import models
from django.contrib.auth.models import User
import uuid


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

    def __str__(self):
        return f"{self.sender} to {self.receiver}"


class MessageHistory(models.Model):
    message_id = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    content = models.TextField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

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
