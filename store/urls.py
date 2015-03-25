from django.conf.urls import patterns, url

from store import views

urlpatterns = patterns('',
    url(r'^$', views.indexView, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^restricted/$', views.restricted, name='restricted'),
    url(r'^restricted/changePassword/$', views.password_change, name='changePassword'),
    )
