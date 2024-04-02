from django.shortcuts import render
from userauths.forms import UserRegistrationForm

# Create your views here.
def register(request):

    if(request.method=="POST"):
        print("User registered")

    else:
        print("User not registered")

    form=UserRegistrationForm()

    context={
        'form':form,
    }
    

    return render(request,'userauths/register.html',context)