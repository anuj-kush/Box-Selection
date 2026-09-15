from django.contrib import admin
from django.urls import path
from shipping import views
urlpatterns = [path("admin/", admin.site.urls), path("", views.home), path("api/recommend/", views.recommend)]
