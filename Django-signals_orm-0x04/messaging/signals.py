from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user_id=instance.receiver, message_id=instance)


@receiver(pre_save, sender=Message)
def message_edits(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message_id=old_message, content=old_message.content
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass
