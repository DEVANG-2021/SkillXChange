from django.db import models
from django.utils import timezone
import pytz
from .customer import Customer

# Define Canada timezone (e.g., Eastern Time)
CANADA_TIMEZONE = pytz.timezone('Canada/Eastern')

def current_canada_date():
    """Get the current date in the Canada timezone."""
    return timezone.now().astimezone(CANADA_TIMEZONE).date()

def current_canada_time():
    """Get the current time in the Canada timezone."""
    return timezone.now().astimezone(CANADA_TIMEZONE).time()

class Meeting(models.Model):
    title = models.CharField(max_length=255)  # Meeting title
    scheduled_by = models.ForeignKey(
        'Customer', on_delete=models.CASCADE, related_name='scheduled_meetings'
    )  # Customer who scheduled the meeting
    participants = models.ManyToManyField(
        'Customer', related_name='invited_meetings'
    )  # Customers invited to the meeting
    participant_emails = models.JSONField(default=list)  # Array of participant emails
    meeting_link = models.URLField()  # Unique meeting link
    meeting_code = models.CharField(max_length=10, unique=True)  # Random meeting code
    date = models.DateField(default=current_canada_date)  # Default to current date in Canada timezone
    time = models.TimeField(default=current_canada_time)  # Default to current time in Canada timezone

    def __str__(self):
        return self.title

    def get_canada_datetime(self):
        """Convert the stored date and time to Canada timezone."""
        # Combine date and time fields into a naive datetime object
        naive_datetime = timezone.datetime.combine(self.date, self.time)

        # Convert naive datetime to the current timezone (default assumed UTC)
        utc_datetime = timezone.make_aware(naive_datetime, timezone.utc)

        # Convert to Canada timezone
        canada_datetime = utc_datetime.astimezone(CANADA_TIMEZONE)

        return canada_datetime

    def save(self, *args, **kwargs):
        """Ensure the date and time are stored as Canada timezone."""
        if self.date and self.time:
            # Combine date and time into a naive datetime object
            naive_datetime = timezone.datetime.combine(self.date, self.time)

            # Convert to Canada timezone
            aware_datetime = CANADA_TIMEZONE.localize(naive_datetime)

            # Convert to UTC for storage (Django default)
            utc_datetime = aware_datetime.astimezone(pytz.utc)

            # Update fields for storage
            self.date = utc_datetime.date()
            self.time = utc_datetime.time()

        super().save(*args, **kwargs)
