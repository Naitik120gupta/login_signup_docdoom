from django.urls import path
from .views import RegisterView, LoginView, PasswordResetView,SetNewPasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set_new_password'),
]
