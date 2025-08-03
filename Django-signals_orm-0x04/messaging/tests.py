from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()

class MessageNotificationTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='alice', password='testpass')
        self.user2 = User.objects.create(username='barbra', password='testpass')

    def test_notification_created_on_new_message(self):
        msg = Message.objects.create()
        notification = Notification.objects.get(message=msg)
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.is_read)
