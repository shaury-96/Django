from django.shortcuts import render

def schedule(request):
    return render(request,'appointments/schedule.html')

def view_appointments(request):
    return render(request,'appointments/view_appointments.html')

def appo(request):
    return render(request,'appointments/appo.html')