from django.utils.timezone import now
from django.db import models
from django.utils import timezone
from .customer import Customer

# Models
class CustomerRating(models.Model):
    rater = models.ForeignKey(Customer, related_name='given_ratings', on_delete=models.CASCADE)
    rated_customer = models.ForeignKey(Customer, related_name='received_ratings', on_delete=models.CASCADE)
    stars = models.IntegerField(default=0)
    comment = models.TextField(blank=True, null=True)
    datetime = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.rater} rated {self.rated_customer} {self.stars} stars"