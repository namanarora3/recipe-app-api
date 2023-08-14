'''
URL mappings for User API
'''
from django.urls import path
from user import views


urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('authenticate/', views.CreateTokenView,name = 'token'),
]

app_name = 'user'