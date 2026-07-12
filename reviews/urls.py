from django.urls import path
from reviews import views

app_name = 'reviews'

urlpatterns = [
    path('create/<int:service_pk>/', views.service_review, name='review_create'),
    #path('<int:pk>/', ..., name='review-detail'),
    #path('user/<int:user_pk>/', ..., name='user-reviews'),
]
