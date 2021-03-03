from rest_framework.views import APIView
from rest_framework.response import Response
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
        return Response({'data:':test})

    def put(self,request, pk=None):
        return Response({'method':"'PUT'"})

    def patch(self,request,pk=None):
        return Response({'method:':'PATCH'})
    def delete(self,request,pk=None):
        return Response({'method':'DELETE'})
    # def get_json(request):
    #     if request.method == "POST":
    #         print(request.POST)
    #         json = JSONForm(request.POST)
    #         return Response({'json: ': json })
