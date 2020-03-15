"""CodeTopia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from .views import *

app_name = "account"

urlpatterns = [
    path('user/login/', CustomLoginView.as_view(), name='user_login'),
    path('user/logout/', CustomLogoutView.as_view(), name='user_logout'),
    path('user/create-account/', CreateUserView.as_view(), name="create_user"),

    path('user/password-reset/', CustomPasswordResetView.as_view(), name="user_password_reset"),
    path('user/password-reset-done/', CustomPasswordResetDoneView.as_view(), name="user_password_reset_done"),
    path('user/password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name="user_password_reset_confirm"),
    path('user/password-reset-complete/', CustomPasswordResetCompleteView.as_view(), name="user_password_reset_complete"),

    path('user/<username>/', PrivateUserDashboard.as_view(), name="user_dashboard"),

    path('user/<username>/profile-update/', ProfileUpdate.as_view(), name="update_profile"),
    path('user/<username>/change-password/', UserPasswordChangeView.as_view(), name="change_user_password"),
]
