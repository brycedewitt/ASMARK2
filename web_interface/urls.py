from django.urls import path

from . import views

app_name = 'web_interface'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:drink_id>/', views.pour, name='pour'),


]
