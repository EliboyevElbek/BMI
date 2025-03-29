from django.urls import path

from accounts.views import RegisterView, UserProfileView, send_mail_for_password, reset_password

urlpatterns = [
    path('registration/', RegisterView.as_view()),
    path('profile/', UserProfileView.as_view()),
    path('send-mail/', send_mail_for_password),
    path('reset-password/', reset_password),
]