from rest_framework.views import APIView
from rest_framework.response import Response
from apiapp import prototype_alg 

# from rest_framework import s
# Create your views here.

class api_views(APIView):

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'access to api',
        ]
        return Response({'message':'Hello!','an_apiview': an_apiview})

    def post(self, request):
        test = request.data
        # return prototype_alg.api_request(test)
        
        #until merged just return this
        return Response(200)
        # return Response({'data:':test})

    def put(self,request, pk=None):
        return Response({'method':"'PUT'"})

    def patch(self,request,pk=None):
        return Response({'method:':'PATCH'})
    def delete(self,request,pk=None):
        return Response({'method':'DELETE'})

# def post_json(request):
#     json = request.POST
#     return 200

