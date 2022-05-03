from multiprocessing import context
import re
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .forms import MyfileUploadForm
from .models import file_upload


def home(request):
    return render(request, "index1.html")

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if User.objects.filter(username=username): 
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Account created Successfully")
        return redirect("signin")
    return render(request,"signup.html")

def signin(request):
    if request.method=="POST":
        username=request.POST['username']
        pass1=request.POST['pass1'] 
        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request,user)
            fname=user.first_name
            print('inif block')
            return render(request,"index.html",{'fname': fname})
        else:
            print('else')
            messages.warning(request, "Incorrect Username/Password") 
            return redirect("home")
    else:
        return render(request, "signin.html")

def signout(request):
    logout(request)
    messages.success(request ,"Logged Out Succefully")
    return redirect("home")

def index(request):
    if request.method == 'POST':
        form = MyfileUploadForm(request.POST, request.FILES)
        print(form.as_p)
        if form.is_valid():
            name = form.cleaned_data['file_name']
            the_files = form.cleaned_data['files_data']
            file_upload(file_name=name, my_file=the_files).save()          
            return HttpResponse("file upload")
        else:
            return HttpResponse('error')
    else:
        context = {
            'form':MyfileUploadForm()
        }        
        return render(request, 'index.html', context)
        



def show_file(request):
    # this for testing 
    all_data = file_upload.objects.all()

    context = {
        'data':all_data 
        }

    return render(request, 'view.html', context)
    


