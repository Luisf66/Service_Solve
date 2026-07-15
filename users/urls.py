from django.urls import path
from users.views import user_views, address_views, telephone_views, auth_views
from users.views.api import user_api_views

app_name = 'users'

urlpatterns = [
    path('register/', auth_views.RegistroView.as_view(), name='register'),

    path('', user_views.UserListView.as_view(), name='user_list'),
    path('create/', user_views.UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/', user_views.UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/update/', user_views.UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', user_views.UserDeleteView.as_view(), name='user_delete'),
    
    path('<int:pk>/addresses/create/', address_views.AddressCreateView.as_view(), name='user_address_create'),
    path('<int:pk>/addresses/<int:address_pk>/update/', address_views.AddressUpdateView.as_view(), name='user_address_update'),
    path('<int:pk>/addresses/<int:address_pk>/delete/', address_views.AddressDeleteView.as_view(), name='user_address_delete'),

    path('<int:pk>/telephones/create/', telephone_views.TelephoneCreateView.as_view(), name='user_telephone_create'),
    path('<int:pk>/telephones/<int:telephone_pk>/update/', telephone_views.TelephoneUpdateView.as_view(), name='user_telephone_update'),
    path('<int:pk>/telephones/<int:telephone_pk>/delete/', telephone_views.TelephoneDeleteView.as_view(), name='user_telephone_delete'),
    
]

urlpatterns += [
    path('api/v1/users/', user_api_views.UserListView.as_view(), name='user_api_list'),
    path('api/v1/users/<int:pk>/', user_api_views.UserDetailView.as_view(), name='user_api_detail'),
]