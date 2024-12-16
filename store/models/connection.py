from django.db import models
from .customer import Customer
from django.utils import timezone

class ConnectionRequest(models.Model):
    STATUS_CHOICES = [
        ("sent", "Sent"),
        ("accepted", "Accepted"),
        ("withdrawn", "Withdrawn"),
        ("rejected", "Rejected"),
    ]
    sender = models.ForeignKey(Customer, related_name="sent_requests", on_delete=models.CASCADE)
    receiver = models.ForeignKey(Customer, related_name="received_requests", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    sent_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# class Notification(models.Model):
#     receiver = models.ForeignKey(Customer, related_name="notifications", on_delete=models.CASCADE)
#     sender = models.ForeignKey(Customer, related_name="notifications_from", on_delete=models.CASCADE)
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Notification from {self.sender} to {self.receiver}: {self.message}"

