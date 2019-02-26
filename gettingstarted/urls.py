from django.urls import path, include, re_path

from django.contrib import admin

import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    re_path("^$", hello.views.index, name="index"),
    re_path('^/hello$', hello.views.index1, name='index1'),
]
