from django.urls import path
from mail import views

app_name='mail'

urlpatterns=[

    path('compose/',views.compose,name='compose'),
    path('inbox/',views.inbox,name='inbox')
]