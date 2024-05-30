from django.urls import path 
from realowner import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home,name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/profile/', views.profile, name='profile'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('edit_personal_details/',views. edit_personal_details, name='edit_personal_details'),
    path('edit-contact-channels/',views. edit_contact_channels, name='edit_contact_channels'),
    path('edit_email/', views.edit_email, name='edit_email'),
    path('edit_password/',views.edit_password,name='edit_password'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('item-list/', views.profile, name='item_list_no_ct'),
    path('item-list/<str:ct>/', views.item_list, name='item_list'),
    path('transfer/<int:item_id>/', views.transfer_item, name='transfer_item'),
    path('create/',views.create_item, name='create_item'),
    path('edit-item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('items/delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('edit_password/', views.edit_password, name='edit_password'),
    
   
   
    


]
