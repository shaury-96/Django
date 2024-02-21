from django.shortcuts import render

def compose(request):
    return render(request,'mail/compose.html')

def inbox(request):
    return render(request,'mail/inbox.html')