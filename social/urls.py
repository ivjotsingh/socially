from django.conf.urls import url
from social.views import signup_view,login_view,feed_view,post_view,Like_view

urlpatterns = [
    url(r'^$',signup_view,name="signUp"),
    url(r'^login/$',login_view,name="login"),
    url(r'^feed/$',feed_view,name="feed"),
    url(r'^post/$', post_view,name="post"),
    url(r'^like/$', Like_view ,name="like"),
    url(r'^login/feed/post/$',post_view,name="post"),

]