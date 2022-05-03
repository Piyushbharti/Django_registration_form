from django.urls import path

from . import views


urlpatterns = [    
    path('', views.home, name="home"),
    path('signin', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('signout', views.signout, name="signout"),
    path('index', views.index, name="index"),
    path('view', views.show_file, name="view")
            
]