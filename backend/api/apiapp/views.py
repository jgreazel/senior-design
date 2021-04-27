from rest_framework.views import APIView
from rest_framework.response import Response
from apiapp import prototype_alg 
from apiapp import adt_alg
from apiapp import prototype_gametheory
import json

# from rest_framework import s
# Create your views here.

class attack_api(APIView):

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'access to api',
        ]
        return Response({'message':'Hello!','an_apiview': an_apiview})

    def post(self, request):
        test = request.data
        x = json.dumps(test)
        print(x)
        return Response(prototype_alg.api_request(x))
        

    def put(self,request, pk=None):
        return Response({'method':"'PUT'"})

    def patch(self,request,pk=None):
        return Response({'method:':'PATCH'})
    def delete(self,request,pk=None):
        return Response({'method':'DELETE'})

class attack_defense_api(APIView):

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'access to api',
        ]
        return Response({'message':'Hello!','an_apiview': an_apiview})

    def post(self, request):
        test = request.data
        x = json.dumps(test) 
        print(x)
        return Response(adt_alg.backendRequest(x))

class game_theory_api(APIView):

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'access to api',
        ]
        return Response({'message':'Hello!','an_apiview': an_apiview})

    def post(self, request):
        test = request.data
        x = json.dumps(test)
        print(x)
        return Response(prototype_gametheory.backendRequest(x))
