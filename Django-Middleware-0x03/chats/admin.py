from django.contrib import admin
from .models import User, Message, Conversation

# Register your models here.
admin.site.register(User)
admin.site.register(Conversation)
admin.site.register(Message)
