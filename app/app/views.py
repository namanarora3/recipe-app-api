from django.shortcuts import redirect

from rest_framework.views import APIView


def redirect_home(request):
  res = redirect('/api/docs')
  return res