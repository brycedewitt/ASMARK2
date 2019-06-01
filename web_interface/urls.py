from django.urls import path
# Use include() to add URLS from the catalog application and authentication system
from django.urls import include
from django.contrib.auth import views as auth_views
from django.conf.urls import url



from . import views

app_name = 'web_interface'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:drink_id>/', views.pour, name='pour'),
    path('pourshot/<int:beverage_id>/', views.pourShot, name='pourShot'),
    path('shots/', views.ShotsView.as_view(), name='shots'),
    path('mix/', views.MixView.as_view(), name='mix'),
]
