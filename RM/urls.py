from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home),
    path('login',views.login),
    path('register',views.register),
    path('feedback',views.feedback),
    path('logout',views.logout),
    path('predict',views.imagePrediction),
]