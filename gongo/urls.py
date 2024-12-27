from django.urls import path
from . import views

app_name = 'gongo'

urlpatterns = [
    path('upload/', views.GongoUploadView.as_view()),
    path('list/', views.GongoListView.as_view()),
    path('detail/<int:pk>/', views.GongoDetailView.as_view()),
    path('addtocart/', views.AddToCartView.as_view()),
    path('cartlist/', views.CartListView.as_view()),
]
