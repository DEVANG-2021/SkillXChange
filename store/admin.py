from django.contrib import admin
from .models.customer import Customer
from .models.orders import Order
from .models.connection import ConnectionRequest
from .models.notifications import Notification
from .models.chat import Message
from .models.meetings import Meeting
from .models.roommembers import RoomMember
from .models.customer_ratings import CustomerRating

admin.site.site_header = "SkillXChange"
admin.site.site_title = "SkillXChange"
admin.site.index_title = "Welcome to the Admin Panel"


# Register your models here.

admin.site.register(Customer)
admin.site.register(ConnectionRequest)
admin.site.register(Notification)
admin.site.register(Message)
admin.site.register(Meeting)
admin.site.register(RoomMember)
admin.site.register(CustomerRating)