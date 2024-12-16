from django.db import models
from .customer import Customer
from .connection import ConnectionRequest
from django.utils import timezone

class Notification(models.Model):
    receiver = models.ForeignKey(Customer, related_name="notifications", on_delete=models.CASCADE)
    sender = models.ForeignKey(Customer, related_name="notifications_from", on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification from {self.sender} to {self.receiver}: {self.message}"