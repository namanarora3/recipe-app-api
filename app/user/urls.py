'''
URL mappings for User API
'''
from django.urls import path, include
from user import views


urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('authenticate/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('image/', views.ImageUpdateView.as_view({'post': 'update'}), name='image'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('generate_otp/', views.ResetPasswordGenerateToken.as_view()),
    path('reset_password/', views.ResetPasswordView.as_view()),
]


app_name = 'user'
