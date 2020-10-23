from django.urls import path
from . import views

urlpatterns = [
    path('qq/login/', views.QQAuthURLView.as_view()),
    path('oauth_callback/', views.QQAuthUserView.as_view()),
]
