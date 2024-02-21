from django.urls import path
from . import views

app_name='food'
urlpatterns = [
    # /food/
    # path('', views.index, name='index'),
    path('',views.IndexClassView.as_view(),name='index'),
    # /food/items/
    path('items/',views.items,name='items'),
    # /food/1
    # path('<int:item_id>/',views.detail,name='detail'),
    path('<int:pk>/',views.FoodDetailView.as_view(),name='detail'),
    # /food/add/
    path('add/',views.CreateItem.as_view(),name='create_item'),
    # food/edit/1
    path('update/<int:id>/',views.update_item,name='update_item'),
    # food/delete/1
    path('delete/<int:id>/',views.delete_item,name='delete_item')
]