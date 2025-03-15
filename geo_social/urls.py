"""
URL configuration for geo_social project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from geo_social_app.views import outbox, note_detail, person, activity_detail

urlpatterns = [
    re_path(r'^@(?P<username>\w+)/notes/(?P<id>\w+)/$', note_detail, name="note_detail"),
    # re_path(r'^@(?P<username>\w+)/notes/$', notes, name="notes"),
    # re_path(r'^@(?P<username>\w+)/following/$', following, name="following"),
    # re_path(r'^@(?P<username>\w+)/followers/$', followers, name="followers"),
    # re_path(r'^@(?P<username>\w+)/inbox/$', inbox, name="inbox"),
    re_path(r'^@(?P<username>\w+)/outbox/(?P<id>\w+)/$', activity_detail, name="activity_detail"),
    re_path(r'^@(?P<username>\w+)/outbox/$', outbox, name="outbox"),
    re_path(r'^@(?P<username>[^/]+)/$', person, name="person"),
    path('admin/', admin.site.urls),
]
