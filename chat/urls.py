from django.urls import path
from chat import views

app_name = 'chat'

urlpatterns = [
    path('<int:service_pk>/messages/', views.message_list, name='message_list'),
    path('<int:service_pk>/messages/send/', views.message_send, name='message_send'),
    path('<int:service_pk>/', views.chat_detail, name='chat_detail'),
]
