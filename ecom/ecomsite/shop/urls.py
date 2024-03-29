from django.urls import path
# from shop.views import index
from shop import views

app_name= 'shopURLs'

urlpatterns=[
    path('',views.index,name='index'),
]