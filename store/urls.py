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
    url(r'^product/(?P<product_id>\d+)/edit/$', views.ProductEdit,name='ProductEdit'),
    url(r'^(?P<user_name>[\w\-]+)/$', views.restricted, name='restricted'),
    url(r'^(?P<user_name>[\w\-]+)/changePassword/$', views.password_change, name='changePassword'),
<<<<<<< HEAD
    
)
=======
    url(r'^(?P<user_name>[\w\-]+)/review/(?P<orderid>[\w\-]+)/$', views.rate_review, name='reviewRate'),
    )
>>>>>>> origin/master
