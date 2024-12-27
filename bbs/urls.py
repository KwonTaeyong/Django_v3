from django.urls import path
from . import views

app_name = 'bbs'

urlpatterns = [
    path('list/', views.BbsList_View.as_view()),
    path('detail/<int:pk>/', views.BbsDetail_View.as_view()),
    path('post/', views.BbsPost_View.as_view()),
]
