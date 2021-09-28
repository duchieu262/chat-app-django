from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Contact, Chat

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        exclude = ['user', 'friends']



class CreateContactForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class ChatForm(ModelForm):
    class Meta:
        model = Chat
        fields = "__all__"
        exclude = ['participants', 'messages']
