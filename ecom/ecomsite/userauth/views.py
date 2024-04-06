from django.shortcuts import render, redirect
from userauth.forms import UserRegistrationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect,requires_csrf_token


# Create your views here.

def register(request):
    if(request.method=="POST"):
        form=UserRegistrationForm(request.POST or None)
        if form.is_valid():
            user=form.save(commit=False)
            first_name=form.cleaned_data['first_name']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password1']
            user.save()
            messages.success(request,f"Hey {first_name}, Your account was created")
            new_user=authenticate(email=email, password=password)
            login(request,new_user)
            return redirect('shop:index')
    else:
        print("User not registered")
        form=UserRegistrationForm()

    # form=UserRegistrationForm()

    context={
        'form':form,
    }
    

    return render(request,'userauth/register.html',context)