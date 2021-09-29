from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:chatId>/', views.room, name='room'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('account/', views.accountSettings, name='account'),
    path('createChat/', views.createChat, name='createChat'),
    path('roomsetting/<int:chatId>/', views.roomSettings, name='roomSettings'),
    path('join/', views.joinRoom, name='joinRoom'),
    path('leave/', views.leaveRoom, name='leaveRoom'),
]
