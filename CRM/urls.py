
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from CRM import views



urlpatterns = [
    url(r'^$', views.index,name='sales_index'),
    url(r'^$', views.customer,name='customer_list'),
    url(r'^$', views.students,name='stu_index'),
]
