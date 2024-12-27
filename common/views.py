import requests
from rest_framework.views import APIView
from rest_framework import status
import smtplib
import json
from email.message import EmailMessage

from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserInfoSerializer, EmailLoginSerializer, EmailSignUpSerializer
from .models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from config.settings import SIMPLE_JWT


# 회원가입
class MailSignUpView(generics.CreateAPIView):
    serializer_class = EmailSignUpSerializer


# 토큰 발급(로그인),갱신
class MailLoginView(generics.GenericAPIView):
    serializer_class = EmailLoginSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            user_info = {
                'last_login': user.last_login,
                'is_staff': user.last_login,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_active': user.last_login,
                'date_joined': user.date_joined,
                'email': user.email
            }
            refresh = RefreshToken.for_user(user)

            REFRESH_TOKEN_LIFETIME = SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
            refresh_expires = REFRESH_TOKEN_LIFETIME.total_seconds() * 1000

            data = {
                'user_info': user_info,
                'refresh_token': str(refresh),
                'refresh_expires': refresh_expires,
            }
            response = Response(data, status=status.HTTP_200_OK)

            return response
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


# 유저정보
class UserInfoView(generics.RetrieveAPIView):
    """
    로그인(토큰) 필수
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserInfoSerializer

    def get_object(self):
        user = self.request.user
        user_info = User.objects.get(id=user.id)
        return user_info


class KakaoLogin(APIView):
    def post(self, request):

        Turl = "https://kauth.kakao.com/oauth/token"
        Theaders = {
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        Tdata = {
            "grant_type": "authorization_code",
            "client_id": "86d6fb1059641a9172f1125c9e026007",
            "redirect_uri": "https://www.example.com/oauth",
            "code": "GnrprfCKrk94ftrPd0RXWL98YuAOskH5h-p9HBllsln8GmumCtpmKSiyXqkKKiUPAAABjenOYKUhI_W2iNNaeg"
        }

        response2 = requests.post(Turl, headers=Theaders, data=Tdata)

        url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

        # 사용자 토큰
        headers = {
            "Authorization": "Bearer " + response2.json().get('access_token')
        }

        data = {
            "object_type": "text",
            "text": "Hello, world!",
            "link": {
                "web_url": "https://www.naver.com"
            },
            'button_title': '키워드'

        }
        data = {'template_object': json.dumps(data)}
        response = requests.post(url, headers=headers, data=data)
        print(response)
        if response.json().get('result_code') == 0:
            print('메시지를 성공적으로 보냈습니다.')
        else:
            print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))

        # MSG = Message(service_key="7cd9570471e83919764b37665bc8d266")
        # auth_url = MSG.get_url_for_generating_code()
        # print(auth_url)
        # url = ""
        # access_token = MSG.get_access_token_by_redirected_url(url)
        # print(access_token)
        # MSG.set_access_token(access_token)
        #
        # message_type = "text"  # 메시지 유형 - 텍스트
        # text = "텍스트 영역입니다. 최대 200자 표시 가능합니다."  # 전송할 텍스트 메시지 내용
        # link = {
        #     "web_url": "https://developers.kakao.com",
        #     "mobile_web_url": "https://developers.kakao.com",
        # }
        # button_title = "바로 확인"  # 버튼 타이틀
        #
        # MSG.send_message_to_me(
        #     message_type=message_type,
        #     text=text,
        #     link=link,
        #     button_title=button_title,
        # )

        # return JsonResponse({'message': '카카오톡 메시지 전송 성공'}, status=200)


class EmailPost(APIView):
    def post(self, request):
        email = request.data.get('email')
        print(email)
        if email:
            message = EmailMessage()
            message.set_content('공고 이메일')
            message["Subject"] = "공고 이메일 알림 테스트입니다."
            message["From"] = "rnjsxodyd231@naver.com"  # 보내는 사람의 이메일 계정
            message["To"] = email

            # 이메일 서버에 연결
            smtp = smtplib.SMTP('smtp.naver.com', 587)
            smtp.starttls()
            smtp.login('rnjsxodyd231@naver.com', 'fnehfvm159!')

            # send_mail 함수를 사용하여 이메일을 보냅니다
            smtp.send_message(message)
            smtp.quit()
            return Response({"succes": "이메일을 성공적으로 보냈습니다."})

        else:
            # 이메일 파라미터가 누락된 경우에는 실패 응답을 반환합니다.
            return Response({"error": "이메일 파라미터가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)
