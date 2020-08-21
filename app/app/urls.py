from django.urls import path
from . import views

urlpatterns = [
    path('users/<uuid:pk>/', views.UserProfileDetail.as_view(), name='user_detail'),
]
