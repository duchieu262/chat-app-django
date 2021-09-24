from django.contrib import admin
from .models import Message, Chat, Contact

admin.site.register((Message, Contact, Chat))
