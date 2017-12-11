from django.conf.urls import url
from  . import views


urlpatterns=[
    url(r'^$', views.index, name="index"),
    url(r'^login/$', views.login, name="login"),
    url(r'^register/$', views.register, name="register"),
    url(r'^cart/$', views.cart, name="cart"),
    url(r'^submit/$', views.submit, name="submit"),
    url(r'^product_detail/(?P<id_sanphamtuychon>[0-9]+)$', views.info, name="info"),
    url(r'^catalog/(?P<id_catalog>[0-9]+)$', views.catalog, name="catalog"),
    url(r'^account/$', views.account, name="account"),
    url(r'^bill/$', views.bill, name="bill"),
    url(r'^bill_info/(?P<id_bill>[0-9]+)$', views.bill_info, name="bill_info"),
    url(r'^change_pass/$', views.change_pass, name="change_pass"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^add/(?P<id>[0-9]+)$',  views.add, name='shopping-cart-add'),
    url(r'^remove/(?P<id>[0-9]+)$', views.remove, name='shopping-cart-remove'),
    url(r'^clear/$', views.clear, name='shopping-cart-clear'),
    url(r'^set_qty/$', views.set_quatity, name='shopping-cart-set-qty'),
    url(r'^search/$', views.search, name='search'),
]
