from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import s
# Create your views here.


def post_json(request):
    json = request.POST
    return 200

