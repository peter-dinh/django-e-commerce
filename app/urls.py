from django.conf.urls import url
from  . import views


urlpatterns=[
    url(r'^$', views.index, name="index"),
    url(r'^login/$', views.login, name="login"),
    url(r'^register/$', views.register, name="register"),
    url(r'^cart/$', views.cart, name="cart"),
    url(r'^product_detail/$', views.info, name="info"),
    url(r'^catalog/$', views.catalog, name="catalog"),
    url(r'^account/$', views.account, name="account"),
    url(r'^bill/$', views.bill, name="bill"),
    url(r'^change_pass$/', views.change_pass, name="change_pass"),
]