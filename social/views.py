# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from social.forms import SignUp_form,Login_form
from social.models import User_model,SessionToken_model
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password,check_password
import ctypes

def signup_view(request):
    if request.method == 'POST':
        form = SignUp_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if set('abcdefghijklmnopqrstuvwxyz').intersection(name) and set('abcdefghijklmnopqrstuvwxyz@_1234567890').intersection(username):
                if len(username)>4 and len(password)>5 :
                    user = User_model(name=name, password=make_password(password), email=email, username=username)
                    user.save()

                    return render(request, 'login.html')
                else:
                    form= SignUp_form()
            else:
                form = SignUp_form()
        else:
            form = SignUp_form()

    else:
        form = SignUp_form()

    return render(request, 'sign_up.html', {'form': form})

def login_view(request):
    data=""
    if request.method=="POST":
        form=Login_form(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=User_model.objects.filter(username=username).first()

            if user:
                if check_password(password,user.password):
                    token=SessionToken_model(user=user)
                    token.createToken()
                    token.save()
                    response=redirect('feed/')
                    response.set_cookie(key='sessionToken', value=token.sessionToken)
                    return response
                    data=""

                else:
                    data="incorrect pass"

    else:
        form=Login_form()


    return render(request,'login.html',{'form': form,'data':data})


def feed_view(request):
    return render(request,'feed.html')