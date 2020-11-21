from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token


from . import views

urlpatterns = [
    path('accounts', views.users),                                      # CREATE USER ACCOUNT | USERS LIST
    path('accounts/activate', views.confirm_account),      # ACTIVATE ACCOUNT
    path('accounts/<uuid>', views.user_RUD),                # UPDATE | READ | DELETE USER
    path('create-token', obtain_auth_token),                      # CREATE AUTH TOKEN
]
