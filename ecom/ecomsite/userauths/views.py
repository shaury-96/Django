from django.shortcuts import render, redirect
from userauths.forms import UserRegistrationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

# Create your views here.
def register(request):

    if(request.method=="POST"):
        form=UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user=form.save()
            username=form.cleaned_data['username']
            messages.success(request,f"Hey {username}, Your account was created")
            new_user=authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request,new_user)
            return redirect('shop:index')
    else:
        print("User not registered")
        form=UserRegistrationForm()

    # form=UserRegistrationForm()

    context={
        'form':form,
    }
    

    return render(request,'userauths/register.html',context)