from django.shortcuts import render, redirect
from userauth.forms import UserRegistrationForm
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from userauth.models import CustomUser


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


def login_view(request):
    
    if request.user.is_authenticated:
        return redirect("shop:index")
    
    if request.method == "POST":
        email=request.POST.get("email")
        password=request.POST.get("password")

        try:
            user=CustomUser.objects.get(email=email)
        except:
            messages.warning(request, f"user with {email} do not exist")

        user=authenticate(request,email=email,password=password)

        if user is not None:
            login(request,user)
            messages.success(request,"you are logged in")
            return redirect("shop:index")
        else:
            messages.warning(request, "Wrong password")

    return render(request,"userauth/login.html")
        
def logout_view(request):
    logout(request)
    return redirect("userauth:login")