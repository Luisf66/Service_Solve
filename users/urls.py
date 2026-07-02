from django.urls import path
from users.views import user_views, address_views, telephone_views

app_name = 'users'

urlpatterns = [
    path('', user_views.UserListView.as_view(), name='user_list'),
    path('create/', user_views.UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/', user_views.UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/update/', user_views.UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', user_views.UserDeleteView.as_view(), name='user_delete'),
    
    path('<int:pk>/addresses/', address_views.AddressListView.as_view(), name='user_addresses'),
    path('<int:pk>/addresses/create/', address_views.AddressCreateView.as_view(), name='user_address_create'),
    path('<int:pk>/addresses/<int:address_pk>/update/', address_views.AddressUpdateView.as_view(), name='user_address_update'),
    path('<int:pk>/addresses/<int:address_pk>/delete/', address_views.AddressDeleteView.as_view(), name='user_address_delete'),

    path('<int:pk>/telephones/', telephone_views.TelephoneListView.as_view(), name='user_telephones'),
    path('<int:pk>/telephones/create/', telephone_views.TelephoneCreateView.as_view(), name='user_telephone_create'),
    path('<int:pk>/telephones/<int:telephone_pk>/update/', telephone_views.TelephoneUpdateView.as_view(), name='user_telephone_update'),
    path('<int:pk>/telephones/<int:telephone_pk>/delete/', telephone_views.TelephoneDeleteView.as_view(), name='user_telephone_delete'),
    
]
