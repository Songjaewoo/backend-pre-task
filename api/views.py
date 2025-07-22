from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactListSerializer
from .models import Contact


class Hello(APIView):
    def get(self, request):
        result = {'data': 'Hello!'}
        return Response(result, status=status.HTTP_200_OK)


class ContactListView(APIView):
    def get(self, request):
        contacts = Contact.objects.all()
        serializer = ContactListSerializer(contacts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


