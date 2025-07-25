from django.urls import path
from .views import SendVerificationCodeView, VerifyCodeView, UserProfileView

urlpatterns = [
    path("send-code/", SendVerificationCodeView.as_view(), name="send-code"),
    path("verify-code/", VerifyCodeView.as_view(), name="verify-code"),
    path("profile/", UserProfileView.as_view(), name="profile"),
]
