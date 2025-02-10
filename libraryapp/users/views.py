from email.message import Message

from django.contrib.auth import authenticate
from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages


def user_login(request):
    if request.method == "POST":
        u = request.POST['u']
        p = request.POST['p']

        # Authenticate the user
        user = authenticate(request, username=u, password=p)

        if user is not None:
            # Log the user in using the correct 'login' function
            auth_login(request, user)
            return redirect('book:home')  # Change this to your actual redirect URL
        else:
            # Invalid credentials, show an error message
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


from django.http import HttpResponse

def register(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        p1=request.POST['p1']
        e=request.POST['e']
        f=request.POST['f']
        l=request.POST['l']
        if(p==p1):
            u= User.objects.create_user(username=u, password=p, email=e, first_name=f, last_name=l)
            u.save()
            return redirect('book:home')

        else:
            messages.error(request,"password are not same")
    return render(request,'register.html')










from django.shortcuts import render

# Create your views here.
