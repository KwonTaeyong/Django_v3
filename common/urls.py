from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

app_name = 'common'

urlpatterns = [
    path('emailSend/', EmailPost.as_view(), name='인증메일'),
    path('emailSignup/', MailSignUpView.as_view(), name='회원가입'),
    path('emailLogin/', MailLoginView.as_view(), name='login'),

    path('kakaoLogin/', KakaoLogin.as_view(), name='kakaopost'),

    path('tokenRefresh/', TokenRefreshView.as_view(), name='토큰 갱신'),

    path('userInfo/', UserInfoView.as_view(), name='유저정보'),
]
