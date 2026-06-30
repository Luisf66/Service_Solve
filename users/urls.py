from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('', views.UserListView.as_view(), name='user_list'),
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    
    #path('<int:pk>/addresses/', ..., name='user-addresses'),
    #path('<int:pk>/addresses/create/', ..., name='user-address-create'),
    #path('<int:pk>/addresses/<int:address_pk>/update/', ..., name='user-address-update'),
    #path('<int:pk>/addresses/<int:address_pk>/delete/', ..., name='user-address-delete'),

    #path('<int:pk>/telephones/', ..., name='user-telephones'),
    #path('<int:pk>/telephones/create/', ..., name='user-telephone-create'),
    #path('<int:pk>/telephones/<int:telephone_pk>/update/', ..., name='user-telephone-update'),
    #path('<int:pk>/telephones/<int:telephone_pk>/delete/', ..., name='user-telephone-delete'),
    
]
