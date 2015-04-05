from django.conf.urls import patterns, url

from store import views

urlpatterns = patterns('',
    url(r'^$', views.indexView, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^search/$', views.create_search, name='create_search'),
    url(r'^product/$', views.ErrorPage, name='ErrorPage'),
    url(r'^product/(?P<product_id>\d+)/$', views.ProductPage,name='ProductPage'),
    url(r'^product/(?P<product_id>\d+)/feedback/$', views.ProductFeedback,name='ProductFeedback'),
    url(r'^product/(?P<product_id>\d+)/purchase/$', views.ProductPurchase,name='ProductPurchase'),
    url(r'^product/(?P<product_id>\d+)/rent/$', views.ProductRent,name='ProductRent'),
    url(r'^user/(?P<user_name>[\w\-]+)/$', views.my_account, name='my_account'),
    url(r'^user/(?P<user_name>[\w\-]+)/changePassword/$', views.password_change, name='changePassword'),
    url(r'^user/(?P<user_name>[\w\-]+)/review/(?P<orderid>[\w\-]+)/$', views.rate_review, name='reviewRate'),
    )
