from django.shortcuts import render,redirect
from .forms import SignUpForm
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from users.models import User

def home(request):
    return render(request, 'users/base.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)  #create user instance without saving
            save_form.set_password(form.cleaned_data['password'])  #hash the password
            save_form.save()
            messages.success(request, 'User registered successfully. Please verify your email.')
            return redirect('login')
        else:
            return render(request, 'users/signup.html', {'form': form}) 
    return render(request, 'users/signup.html', {'form': SignUpForm()})


def activate_mail(request, uidb64, token):
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(id=uid)  
        if user is not None: 
            user.is_verified = True  
            user.save() 
            messages.success(request, 'Email confirmation done successfully')
            return redirect('login')
    except User.DoesNotExist: 
         messages.error(request,"Please sign up") 
         return redirect('signup')

def Login(request):
    return render(request, 'users/login.html')
