from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('company/', views.company, name='company'),
    path('news/', views.news, name='news'),
    path('daily/', views.daily, name='daily'),
    path('dashboard/', views.dashboard, name='dashboard')
]
