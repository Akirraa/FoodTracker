from django.shortcuts import render, redirect 
from .forms import CustomUserCreationForm, LoginForm #importit custom form lel sign up (bch nzid login)
from datetime import date #hedhi bch ne7seb beha age
from django.urls import reverse_lazy
from django.contrib.auth import login as auth_login 
from django.views import View
from django.contrib.auth import logout as auth_logout



#signup views

def calculate_age(birth_date): #just bch ne7sbou age
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def register(request): 
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid(): #ken signup form mte3i valid nhezou ya3ml login
            user = form.save(commit=False)
            birth_date = form.cleaned_data['birth_date']
            user.age = calculate_age(birth_date)
            user.save()
            return redirect('login') 
    else:
        form = CustomUserCreationForm()
        context = {
        'form': form,
        'hide_navbar': True,
    } 
    return render(request, 'authentification/signup.html', context)



#login view
def login(request):
    form = LoginForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect(reverse_lazy('home'))
    
    context = { 'form': form,
                'hide_navbar': True,}

    return render(request, 'authentification/login.html', context)

# logout view
def logout(request):
    auth_logout(request)  
    return redirect('home') 
