#python
#django
#api
#apps
import sendgrid
from sendgrid.helpers.mail import *
from django.shortcuts import render, redirect
from forms import SignUpForm, LoginForm, PostForm, LikeForm, CommentForm
from models import UserModel, SessionToken, PostModel, LikeModel, CommentModel,TagModel,FetchModel
from django.contrib.auth.hashers import make_password, check_password
#for mailing through settings
#from django.core.mail import send_mail
#from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from django.http import HttpResponse
from socially.settings import BASE_DIR
from keys import YOUR_CLIENT_ID,YOUR_CLIENT_SECRET
from imgurpython import ImgurClient
from clarifai.rest import ClarifaiApp
from paralleldots import sentiment,set_api_key
CLARIFAI_API_KEY = 'f3a37216201f4c3faae31795abd09ee6'
app = ClarifaiApp(api_key=CLARIFAI_API_KEY)
from socially.cre import SENDGRID_API_KEY
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # saving data to DB
            user = UserModel(name=name, password=make_password(password), email=email, username=username)
            user.save()

            #optional
            #send_mail(subject,message,from_email,to_list,fail_silently=True)
            # subject="Thankyou for signing up"
            # message="you will enjoy our services \n we will in touch soon"
            # from_email=settings.EMAIL_HOST_USER
            # to_list =[user.email]
            # send_mail(subject,message,from_email,to_list,fail_silently=True)
            # #return render(request, 'login.html')
            return redirect('/social/login/')
    else:
        form = SignUpForm()

    return render(request, 'sign_up.html', {'form': form})


def login_view(request):
    response_data = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = UserModel.objects.filter(username=username).first()

            if user:
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('/social/feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    response_data['message'] = 'Incorrect Password! Please try again!'

    elif request.method == 'GET':
        form = LoginForm()

    response_data['form'] = form
    return render(request, 'login.html', response_data)


def post_view(request):
    user = check_validation(request)

    if user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user=user, image=image, caption=caption)
                post.save()

                path = str(BASE_DIR + post.image.url)

                client = ImgurClient(YOUR_CLIENT_ID, YOUR_CLIENT_SECRET)
                post.image_url = client.upload_from_path(path, anon=True)['link']
                post.save()
                model = app.models.get('general-v1.3')  # notify model which we are going to use from clarifai
                response = model.predict_by_url(url=post.image_url)  # pass the url of current image

                if response["status"]["code"] == 10000:
                    if response["outputs"]:
                        if response["outputs"][0]["data"]:
                            if response["outputs"][0]["data"]["concepts"]:

                                for index in range(0, len(response["outputs"][0]["data"]["concepts"])):
                                    hash = TagModel(tag_text=response["outputs"][0]["data"]["concepts"][index]["name"])

                                    hash.save()
                                    fetch=FetchModel(id_of_tag=hash,id_of_post=post)
                                    fetch.save()
                                return redirect('/social/feed/')

        else:
            form = PostForm()
        return render(request, 'post.html', {'form': form})
    else:
        return redirect('/login/')


def feed_view(request):
    user = check_validation(request)
    if user:
        posts = PostModel.objects.all().order_by('-created_on')

        for post in posts:
            existing_like = LikeModel.objects.filter(post=post.id, user=user).first()
            if existing_like:
                post.has_liked = True

            comments=CommentModel.objects.filter(post=post.id)
            pos = 0
            neg = 0
            for comment in comments:

                if comment.review>=0.6:
                    pos+=1

                else:
                    neg+=1
            print pos
            if pos>neg:
                post.has_recommended=True
            else:
                post.has_recommended=False

        return render(request, 'feed.html', {'posts': posts})
    else:

        return redirect('/social/login/')

#retriving images based on analysis of content
def tag_view(request):
    user = check_validation(request)
    if user:
        q = request.GET.get('q')
        hash= TagModel.objects.filter(tag_text = q).first()
        posts = FetchModel.objects.filter(id_of_tag=hash)
        posts=[post.id_of_post for post in posts]
        if (posts == []):
            return HttpResponse("<H1><CENTER>NO SUCH TAG FOUND</H1>")
        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True
        return render(request, 'feed.html', {'posts': posts})
    else:
        return redirect('/social/login/')

def tag_view_u(request,hash_tag):
    user = check_validation(request)
    if user:

        hash= TagModel.objects.filter(tag_text = hash_tag).first()
        posts = FetchModel.objects.filter(id_of_tag=hash)
        posts=[post.id_of_post for post in posts]
        if (posts == []):
            # make a 404 page and render it
            return HttpResponse("<H1><CENTER>NO SUCH TAG FOUND</H1>")
        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True
        return render(request, 'feed.html', {'posts': posts})
    else:
        return redirect('/social/login/')

def user_view(request):
    user=check_validation(request)

    if user:
        query=request.GET.get('q')
        user=UserModel.objects.filter(username=query).first()
        posts=PostModel.objects.filter(user=user)
        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True
        return render(request, 'feed.html', {'posts': posts})
    else:
        return redirect('/social/login/')

def user_view_u(request,user_name):
    user=check_validation(request)

    if user:
        user=UserModel.objects.filter(username=user_name).first()
        posts=PostModel.objects.filter(user=user)
        #not_neccessary to make list
        posts=[post for post in posts]
        if posts==[]:
            #make a 404 page and render it
            return HttpResponse("<h1>No such user found</h1>")
        else:
            for post in posts:
                existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
                if existing_like:
                    post.has_liked = True
            return render(request, 'feed.html', {'posts': posts})
    else:
        return redirect('/social/login/')


def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()
            return redirect('/social/feed/')
    else:
        return redirect('/social/login/')


def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = str(form.cleaned_data.get('comment_text'))
            set_api_key('qvGZYufnXUmQNxbFi6h4GDlNtu30HKzhFxJvMUnAdNc')
            review=sentiment(comment_text)

            if review['sentiment']:
                comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text,review=review['sentiment'])
                comment.save()
                return redirect('/social/feed/')
        else:
            return redirect('/social/feed/')
    else:
        return redirect('/social/login/')

def logout_view(request):
    request.session.modified = True
    response = redirect('/social/login/')
    response.delete_cookie(key='session_token')
    return response

# For validating the session
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            time_to_live = session.created_on + timedelta(days=1)
            if time_to_live > timezone.now():
                return session.user
    else:
        return None