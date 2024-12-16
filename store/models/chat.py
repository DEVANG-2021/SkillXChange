from django.db import models
from .customer import Customer  # Assuming the Customer model is in the same app

class Message(models.Model):
    sender = models.ForeignKey(Customer, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Customer, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.first_name} to {self.receiver.first_name} at {self.timestamp}"
