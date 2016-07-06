"""uestc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from subject import views

urlpatterns = [
    url(r'^admin/$', views.admin_login, name='admin_login'),
    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^index/$', views.index, name='index'),
    url(r'^admin/index/$', views.admin_index, name='admin_index'),
    url(r'^course/$', views.get_course, name='get_course'),
    url(r'^log/$', views.get_log, name='get_log'),
    url(r'^choose/$', views.get_already_choose, name='get_already_choose'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^select/$', views.select_course, name='select_course'),
    url(r'^cancel/$', views.cancel_course, name='cancel_course'),
    url(r'^admin/get/course/$', views.list_course, name='list_course'),
    url(r'^admin/get/student/$', views.list_student, name='list_student'),
    url(r'^admin/get/teacher/$', views.list_teacher, name='list_teacher'),
    url(r'^admin/delete/course/$', views.delete_course, name='delete_course'),
    url(r'^admin/add/course/$', views.add_course, name='add_course'),
    url(r'^admin/add/student/$', views.add_student, name='add_student'),
    url(r'^admin/resetPassword/$', views.reset_passwd, name='reset_passwd'),
    url(r'^admin/delete/teacher/$', views.delete_teacher, name='delete_teacher'),
    url(r'^admin/add/teacher/$', views.add_teacher, name='add_teacher'),
    url(r'^search/$', views.search, name='search'),
    url(r'^password/$', views.change_passwd, name='change_passwd'),
]
