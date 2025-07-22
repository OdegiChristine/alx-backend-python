import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        GUEST = 'guest', 'Guest'
        HOST = 'host', 'Host'
        ADMIN = 'admin', 'Admin'

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.GUEST)
    created_at = models.DateTimeField(auto_now_add=True)

    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['email', 'last_name', 'first_name']


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants_id = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    #recipient_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)


class Property(models.Model):
    property_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="properties")
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price_per_night = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELED = 'canceled', 'Canceled'

    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)


class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = 'credit_card', 'Credit Card'
        PAYPAL = 'paypal', 'Paypal'
        STRIPE = 'stripe', 'Stripe'

    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CREDIT_CARD)


class Review(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
