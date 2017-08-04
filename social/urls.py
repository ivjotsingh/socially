from django.conf.urls import url
from social.views import signup_view,login_view,feed_view,post_view,like_view,comment_view,tag_view,tag_view_u,user_view,user_view_u,logout_view

urlpatterns = [

    url(r'^$',signup_view,name="signUp"),
    url(r'^login/$',login_view,name="login"),
    url(r'^feed/$',feed_view,name="feed"),
    url(r'^post/$', post_view,name="post"),
    url(r'^like/$', like_view ,name="like"),
    url(r'^comment/$',comment_view,name="comment"),
    url(r'^feed/tag$', tag_view,name="tag"),
    url(r'^feed/tag/(?P<hash_tag>.+)$', tag_view_u,name="tagu"),
    url(r'^feed/user$', user_view,name="user"),
    url(r'^feed/user/(?P<user_name>.+)$', user_view_u,name="useru"),
    url(r'^logout/$', logout_view,name="logout"),

]