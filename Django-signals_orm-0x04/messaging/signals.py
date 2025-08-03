from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()

@receiver(post_delete, sender=User)
def delete_related_user_data(sender, instance, **kwargs):
    MessageHistory.objects.filter(original_message__sender=instance).delete()
    MessageHistory.objects.filter(original_message__receiver=instance).delete()

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.created(
            user=instance.receiver,
            message=instance,
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_instance.content != instance.content:
        MessageHistory.objects.create(
            original_message=old_instance,
            old_content=instance.content,
        )
        instance.edited = True
