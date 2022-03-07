from django.urls import path
from accounts import views  

urlpatterns = [
    path("login/",views.LoginView.as_view(),name="account_login"),
    path("logout/",views.LogoutView.as_view(),name="account_logout"),
    path("signup/",views.LoginView.as_view(),name="account_login")
]