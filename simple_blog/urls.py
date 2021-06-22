"""simple_blog URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from markdownx import urls as markdownx

urlpatterns = [
    path('markdownx/', include(markdownx)),
    path('admin/', admin.site.urls),
]
