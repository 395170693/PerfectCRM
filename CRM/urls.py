
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from CRM import views



urlpatterns = [
    url(r'^$', views.index,name='sales_index'),
    url(r'customer/(\d+)/enrollment/$', views.enrollment,name='enrollment'),
    url(r'^customers$', views.customer_list,name='customer_list'),
    # url(rnt$', views.student,name='stu_index'),
]
