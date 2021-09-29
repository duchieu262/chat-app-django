import json
from django.db import models
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import *
from .forms import ChatForm, CreateContactForm, ContactForm
from .decorators import unauthenticated_user


@unauthenticated_user
def registerPage(request):
    form = CreateContactForm()
    
    if request.method == 'POST':
        form = CreateContactForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = user.username
            Contact.objects.create(user=user, name=username)
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or password incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def index(request):
    contact = Contact.objects.get(user=request.user)
    roomMenu = getRoomMenu(request.user)
    chatId = 1
    if roomMenu:
        chatId = roomMenu[0]['id']
    return render(request, 'chat/index.html', {
        # 'chatId': chatId,
        # 'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
        'roomMenu': getRoomMenu(request.user),
        'contact': contact,
    })

@login_required(login_url='login')
def room(request, chatId):
    contact = Contact.objects.get(user=request.user)
    chat = Chat.objects.get(id=chatId)
    participants = chat.participants.all()
    return render(request, 'chat/chat.html', {
        'chat': chat,
        # 'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
        'roomMenu': getRoomMenu(request.user),
        'contact': contact,
        'participants': participants
    })



@login_required(login_url='login')
def accountSettings(request):
    contact = Contact.objects.get(user=request.user)
    form = ContactForm(instance=contact)
    
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {
        'form': form,
        'contact': contact,
    }
    return render(request, 'accounts/account_settings.html', context)

def getRoomMenu(user):
    roomMenu = []
    contact = Contact.objects.get(user=user)
    chats = Chat.objects.filter(participants=contact)
    for chat in chats:
        lastMessage = getLastMessage(chat)
        room = {
            'id': chat.id,
            'chatName': chat.chatName,
            'chatImg': chat.chatImg,
        }
        roomMenu.append(room)
    return roomMenu

def getLastMessage(chat):
    messages = chat.messages.all()
    if messages:
        lastMessage = messages.last().content
    else:
        lastMessage = "Start chat"
    return lastMessage


def createChat(request):
    contact = Contact.objects.get(user=request.user)
    if request.method == 'POST':
        try:
            userAdds = request.POST.getlist('userAdds')
            chat = Chat.objects.create(chatName=request.POST['chatName'])
            user = Contact.objects.get(user=request.user)
            chat.participants.add(user)
            for userAdd in userAdds:
                userAdd = Contact.objects.get(id=userAdd)
                chat.participants.add(userAdd)
            chat.save()
            return redirect('room',chat.id)
        except:
            return redirect('index')    
    contacts = Contact.objects.exclude(user=request.user)
    return render(request, 'chat/list.html', {
        'contacts':contacts,
        'roomMenu': getRoomMenu(request.user),
        'contact': contact
        })

@login_required(login_url='login')
def roomSettings(request, chatId):
    chat = Chat.objects.get(id=chatId)
    form = ChatForm(instance=chat)
    
    if request.method == 'POST':
        form = ChatForm(request.POST, request.FILES, instance=chat)
        if form.is_valid():
            form.save()
            return redirect('room', chat.id)

    context = {
        'form': form,
        'chat': chat
    }
    return render(request, 'chat/room_settings.html', context)

@login_required(login_url='login')
def joinRoom(request):
    chatId = request.POST['chatId']
    if request.method == 'POST':
        try:
            chat = Chat.objects.get(id=chatId)
            contact = Contact.objects.get(user=request.user)
            chat.participants.add(contact)
            return redirect('room', chatId)
        except:
            return HttpResponse("NOt found")
        

@login_required(login_url='login')
def leaveRoom(request):
    if request.method == 'POST':
        chat = Chat.objects.get(id=request.POST['chatId'])
        contact = Contact.objects.get(user=request.user)
        chat.participants.remove(contact)
        return redirect('index')