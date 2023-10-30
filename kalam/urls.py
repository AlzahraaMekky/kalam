"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.Home, name='home'),
    path('signUp/', views.signUp_CoffeeOwner, name='signUpCoffeeOwner'),
    path('login/', views.Login, name='login') ,
    path('coffee/', views.CoffeeOwner, name='coffee') ,
    path('addsession/', views.AddcoffeeSession, name='addcoffeesession'),
    path('sessionspage/', views.sessionPage, name='sessions'),
    path('signUpUser/', views.signUp_User, name='signUpUser'),
    path('user/', views.UserPage, name='user'),
    path('book/', views.bookSession, name='book'),
    path('checkprofile/', views.checkProfile, name='checkprofile'),
    path('logout/', views.Logout, name='logout'),
    path('deleteBook/', views.deleteBookingSession, name='deleteBook'),
    path('deletesession/<int:id>', views.deleteSession, name='deletesession'),
    path('addTestimonial/', views.addTestimonial, name='addtestimonial') ,


    

    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)