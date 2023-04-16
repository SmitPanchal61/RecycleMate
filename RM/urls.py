from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home),
    path('login',views.login),
    path('register',views.register),
    path('feedback',views.feedback),
    path('logout',views.logout),
    path('predict',views.imagePrediction),
    path('profile',views.profile),
    path('addItem',views.addItem),
    path('delete/<int:imgId>',views.deleteItem),
    path('resources', views.resources),
    path('userstats', views.userStats),
    path('findUser', views.findUser),
    path('findSociety', views.findSociety),
    path('<int:userId>', views.viewItems),
]