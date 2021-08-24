from django import forms
from django.http import request
from django.shortcuts import render
from .forms import UserForm,UserInfoForm
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
#urlresolvers import reverse
# Create your views here.
def index(res):
    return render(res,"base_app/index.html")
@login_required
def special(res):
    return HttpResponse("<h1>You Logged in as a Special User</h1>")
@login_required
def user_logout(res):
    logout(res)
    return HttpResponseRedirect(reverse('index'))
def register(res):
    registered=False
    if res.method=='POST':
        u_form=UserForm(data=res.POST)
        p_form=UserInfoForm(data=res.POST)

        if u_form.is_valid and p_form.is_valid:
            user=u_form.save()
            user.set_password(user.password)
            user.save()
            profile=p_form.save(commit=False)
            profile.user=user

            if 'profile_pic' in res.FILES:
                profile.profile_pic=res.FILES['profile_pic']
            profile.save()

            registered=True
        else:
            print(u_form.errors,p_form.errors)
    else:
        u_form=UserForm()
        p_form=UserInfoForm()

    return render(res,'base_app/register.html',{'uform':u_form,'pform':p_form,'registered':registered})
def user_login(res):
    if res.method=='POST':
        username=res.POST.get('username')
        password=res.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(res,user)
                print("Username : {} \nPassword : {} \n{}".format(username,password,user))
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("<h1>Account is not active!</h2>")
        else:
            print("Some one trying to login!")
            print("Username : {} \nPassword : {}".format(username,password))
            print("Invalid User details is supplied!")
            return HttpResponse("<h1>Account is not found!</h2><a href='dl5_app:user_login'>Click here to go back to login page!</a>")           
    else:
        return render(res,'base_app/login.html',{})
