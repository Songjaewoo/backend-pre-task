from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ParseError, NotFound, ValidationError
from .serializers import ContactListSerializer, LabelSerializer, LabelMapSerializer, ContactDetailSerializer
from .models import Contact, LabelMap, Label


class ContactPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 20


class ContactListView(APIView):
    def get(self, request):
        try:
            sort_field = request.query_params.get('sort_by', 'id')
            sort_order = request.query_params.get('sort_order', 'asc')

            # 기본 출력은 등록 순서대로 정렬
            # 이름, 이메일, 전화번호 중 하나를 선택하여 정렬
            sort_fields = ['name', 'email', 'phone', 'id']
            if sort_field not in sort_fields:
                sort_field = 'id'

            if sort_order == 'desc':
                order_by = f'-{sort_field}'
            else:
                order_by = sort_field

            contacts = Contact.objects.all().order_by(order_by)
            paginator = ContactPagination()
            page = paginator.paginate_queryset(contacts, request)
            serializer = ContactListSerializer(page, many=True)

            return paginator.get_paginated_response(serializer.data)
        except NotFound as e:
            return Response({'message': '페이지를 찾을 수 없습니다'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'message': '예상치 못한 서버 오류'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = ContactDetailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'message': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except ParseError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'message': '예상치 못한 서버 오류'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContactDetailView(APIView):
    def get(self, request, id):
        try:
            contact = Contact.objects.get(id=id)
            serializer = ContactDetailSerializer(contact)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Contact.DoesNotExist:
            return Response({"message": "존재하지 않는 id 입니다"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'message': '예상치 못한 서버 오류'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            contact = Contact.objects.get(id=id)
            serializer = ContactDetailSerializer(contact, data=request.data)
            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'message': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except ParseError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Contact.DoesNotExist:
            return Response({"message": "존재하지 않는 id 입니다"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"message": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
