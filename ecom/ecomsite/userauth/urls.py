from django.urls import path
# from shop.views import index
from userauth import views

app_name= 'userauth'

urlpatterns=[
    path('',views.register,name='register'),
]