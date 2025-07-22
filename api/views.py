from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class Hello(APIView):
    def get(self, request):
        result = {'data': 'Hello!'}
        return Response(result, status=status.HTTP_200_OK)

