
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CreateUserForm

from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User

from django.views.generic import (
    CreateView, 
    ListView, 
    UpdateView, 
    DetailView, 
    DeleteView
)


def registerView(request):
    form = CreateUserForm()
    if request.method == 'POST': 
        form =CreateUserForm(request.POST)
        if form.is_valid(): 
            form.save() 
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"] 
            user = authenticate(username=username,  password=password, email=email)
            login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect('profile')
    else:
        form = CreateUserForm()          
    return render(request, 'registration/signup.html', {'form':form})


class UserEditView(UpdateView):
    model = User 
    form_class = UserChangeForm
    template_name = 'registration/editprofile.html'
    success_url = reverse_lazy("profile")