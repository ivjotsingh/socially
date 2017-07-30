from __future__ import unicode_literals
from social.forms import SignUp_form,Login_form,Post_form,Like_form
from social.models import User_model,SessionToken_model,Post_model,Like_model
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password,check_password
from socially.settings import BASE_DIR
from imgurpython import ImgurClient
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

                    return render(request,'login.html')
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
    response_data = {}
    if request.method == "POST":
        form = Login_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User_model.objects.filter(username=username).first()

            if user:
                if check_password(password, user.password):
                    token = SessionToken_model(user=user)
                    token.createToken()
                    token.save()
                    response = redirect('/social/feed/')
                    response.set_cookie(key='sessionToken', value=token.sessionToken)
                    return response
                else:
                    response_data['message'] = 'Incorrect Password! Please try again!'

    elif request.method == 'GET':
        form = Login_form()

    response_data['form'] = form
    return render(request, 'login.html', response_data)


def feed_view(request):
    user=check_validation(request)
    if user:
        posts=Post_model.objects.all()
        return render(request,'feed.html',{'posts':posts})


def check_validation(request):
    if request.COOKIES.get('sessionToken'):
        session = SessionToken_model.objects.filter(sessionToken=request.COOKIES.get('sessionToken')).first()
        if session:
            return session.user
    else:
        return None

def post_view(request):
    user=check_validation(request)
    if user:
        if request.method=="POST":
            form=Post_form(request.POST,request.FILES)
            if form.is_valid():
                caption=form.cleaned_data['caption']
                image=form.cleaned_data['image']
                post=Post_model(user=user,caption=caption,image=image)
                post.save()
                path=str(BASE_DIR + post.image.url)
                YOUR_CLIENT_ID = "0002161fe35de3d"
                YOUR_CLIENT_SECRET = "f45b827e48c1444021046778a2c3e3e573432709"
                client = ImgurClient(YOUR_CLIENT_ID, YOUR_CLIENT_SECRET)
                post.image_url = client.upload_from_path(path, anon=True)['link']
                post.save()
                return redirect('/social/feed/')

        else:
            form=Post_form()

        return render(request,'post.html',{'form': form})
    else:
        return redirect('/social/login/')


def Like_view(request):
    user=check_validation(request)
    if user:
        if request.method=='POST':
            form=Like_form(request.POST)
            if form.is_valid():
                post_id=form.cleaned_data.get('post').id
                existing_like=Like_model.object.filter(user=user,post=post_id)
                if existing_like:
                    existing_like.delete()
                else:
                    like=Like_model.object.create(user=user,post=post_id)
                    like.save()
    else: