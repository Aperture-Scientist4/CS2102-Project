from django.conf.urls import patterns, url

from store import views

urlpatterns = patterns('',
    url(r'^$', views.indexView, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^search/$', views.create_search, name='create_search'),
    url(r'^product/$', views.ErrorPage, name='error'),
    url(r'^product/(?P<product_id>\d+)/$', views.ProductPage,name='product'),
    url(r'^product/(?P<product_id>\d+)/feedback/$', views.ProductFeedback,name='feedback'),
    url(r'^product/(?P<product_id>\d+)/purchase/$', views.ProductPurchase,name='purchase'),
    url(r'^product/(?P<product_id>\d+)/rent/$', views.ProductRent,name='rent'),
    url(r'^myaccount/$', views.my_account, name='my_account'),
    url(r'^password/$', views.password_change, name='change_password'),
    )
