from django.urls import path
# from shop.views import index
from userauth import views

app_name= 'userauth'

urlpatterns=[
    path('register/',views.register,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout')
]