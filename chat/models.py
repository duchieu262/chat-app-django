from django.db import models
from django.contrib.auth import get_user_model


from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True

class Contact(models.Model):
    user = models.OneToOneField(User, related_name='friends', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="profile1.png", null=True)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    contact = models.ForeignKey(Contact, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.user.username

    def last_10_messages():
        return Message.objects.order_by('timestamp').all()[:10]


class Chat(models.Model):
    participants = models.ManyToManyField(Contact, related_name='chats')
    chatName = models.CharField(max_length=100, blank=True, null=True)
    chatImg = models.ImageField(default="chat.jpg", null=True)
    messages = models.ManyToManyField(Message, blank=True)

    def last_10_messages(self):
        # return self.messages.objects.order_by('-timestamp').all()[:10]
        return self.messages.order_by('timestamp').all()

    def __str__(self):
        return "{}".format(self.pk)
