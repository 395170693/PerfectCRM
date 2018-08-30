
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from king_admin import views



urlpatterns = [
    url(r'^$', views.index,name='table_index'),
    url(r'^(\w+)/(\w+)/$', views.display_table_objs,name='table_objs'),
    url(r'^(\w+)/(\w+)/(\d+)/change/$', views.table_objs_change,name='table_objs_change'),
    url(r'^(\w+)/(\w+)/add/$', views.table_objs_add,name='table_objs_add'),
]
