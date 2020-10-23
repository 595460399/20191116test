from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('info/', views.UserInfoView.as_view(), name='info'),
    path('usernames/<username>/', views.UsernameCountView.as_view()),
    path('mobiles/<mobile>/', views.MobileCountView.as_view()),
    path('emails/', views.EmailView.as_view()),
    path('emails/verification/', views.VerifyEmailView.as_view()),
    path('addresses/', views.AddressView.as_view(), name='address'),
    path('addresses/create/', views.AddressCreateView.as_view()),
    path('addresses/<int:address_id>/', views.UpdateDestoryAddressView.as_view()),
    path('addresses/<int:address_id>/default/', views.DefaultAddressView.as_view()),
    path('addresses/<int:address_id>/title/', views.UpdateTitleAddressView.as_view()),
    path('user_center_pass/', views.ChangePasswordView.as_view(), name='password'),
    # re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})$', views.UsernameCountView.as_view()),
]
