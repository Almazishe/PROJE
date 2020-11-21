from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include([
        path('v1/', include([                                                     # V1 of API's
            path('auth/', include('apps.accounts.api.urls') ),          #  ACCOUNTS URLS /apps/accounts/api/
        ])),
    ]))
]
