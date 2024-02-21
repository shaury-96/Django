from django.urls import path
from appointments import views

app_name='appointments'

urlpatterns=[

    path('schedule/',views.schedule,name='schedule'),
    path('view_appointments/',views.view_appointments,name='view_appointments'),
    path('appo/',views.appo,name='appo')
]