from django.conf.urls import url
from social.views import signup_view,login_view,feed_view

urlpatterns = [
    url(r'^$',signup_view,name="signUp"),
    url(r'^login/$',login_view,name="login"),
    url(r'^login/feed/$',feed_view,name="feed"),
]