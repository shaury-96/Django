from django.urls import path
# from shop.views import index
from shop import views

app_name= 'shop'

urlpatterns=[
    path('',views.index,name='index'),
    path('products/<cid>/',views.product_list,name='product_list')
]