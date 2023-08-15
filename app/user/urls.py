'''
URL mappings for User API
'''
from django.urls import path
from user import views


urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('authenticate/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me')
]


app_name = 'user'
