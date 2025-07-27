from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ParseError, NotFound, ValidationError
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .serializers import ContactListSerializer, LabelSerializer, LabelMapSerializer, ContactDetailSerializer
from .models import Contact, LabelMap, Label
import logging

logger = logging.getLogger(__name__)

class ContactPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 20


class ContactListView(APIView):
    @extend_schema(
        operation_id='contact_list',
        summary='연락처 목록 조회',
        description='연락처를 페이징 처리하여 조회합니다. 등록순, 이름, 이메일, 전화번호로 정렬 가능합니다.',
        parameters=[
            OpenApiParameter(
                name='sort_by',
                description='정렬 기준 필드 (name, email, phone, id)',
                required=False,
                type=OpenApiTypes.STR,
                default='id'
            ),
            OpenApiParameter(
                name='sort_order',
                description='정렬 순서 (asc, desc)',
                required=False,
                type=OpenApiTypes.STR,
                default='asc'
            ),
            OpenApiParameter(
                name='page',
                description='페이지 번호',
                required=False,
                type=OpenApiTypes.INT,
                default=1
            ),
            OpenApiParameter(
                name='size',
                description='페이지 크기 (최대 20)',
                required=False,
                type=OpenApiTypes.INT,
                default=10
            ),
        ],
        responses={
            200: ContactListSerializer(many=True),
            404: OpenApiExample('페이지를 찾을 수 없습니다'),
            500: OpenApiExample('예상치 못한 서버 오류')
        },
    )
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
            logger.error(e)
            return Response({'message': '예상치 못한 서버 오류'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id='contact_create',
        summary='연락처 생성',
        description='새로운 연락처를 생성합니다.',
        request=ContactDetailSerializer,
        responses={
            201: ContactDetailSerializer,
            400: OpenApiExample('잘못된 요청 데이터'),
            500: OpenApiExample('예상치 못한 서버 오류')
        },
        examples=[
            OpenApiExample(
                'Contact Creation Example',
                value={
                    'name': '홍길동',
                    'profile_image_url': 'http://image.jpg',
                    'email': 'hong@example.com',
                    'phone': '010-1234-5678',
                    'company': '키즈노트',
                    'job_title': '팀원',
                    'memo': '수린이',
                    'address': '강남구 논현동',
                    'birthday': '1987-11-18',
                    'website': 'http://www.honggil.dong',
                    'label_names': ['친구', '개발자']
                }
            )
        ],
    )
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
            logger.error(e)
            return Response({'message': '예상치 못한 서버 오류'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContactDetailView(APIView):
    @extend_schema(
        operation_id='contact_detail',
        summary='연락처 상세 조회',
        description='특정 ID의 연락처 상세 정보를 조회합니다.',
        parameters=[
            OpenApiParameter(
                name='id',
                description='연락처 ID',
                required=True,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH
            ),
        ],
        responses={
            200: ContactDetailSerializer,
            404: OpenApiExample('존재하지 않는 id 입니다'),
            500: OpenApiExample('예상치 못한 서버 오류')
        },
    )
    def get(self, request, id):
        try:
            contact = Contact.objects.get(id=id)
            serializer = ContactDetailSerializer(contact)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Contact.DoesNotExist:
            return Response({"message": "존재하지 않는 id 입니다"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(e)
            return Response({'message': '예상치 못한 서버 오류'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id='contact_update',
        summary='연락처 수정',
        description='특정 ID의 연락처 정보를 수정합니다.',
        parameters=[
            OpenApiParameter(
                name='id',
                description='연락처 ID',
                required=True,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH
            ),
        ],
        request=ContactDetailSerializer,
        responses={
            200: ContactDetailSerializer,
            400: OpenApiExample('잘못된 요청 데이터'),
            404: OpenApiExample('존재하지 않는 id 입니다'),
            500: OpenApiExample('예상치 못한 서버 오류')
        },
        examples=[
            OpenApiExample(
                'Contact Update Example',
                value={
                    'name': '김철수',
                    'email': 'kim@example.com',
                    'phone': '010-9876-5432',
                }
            )
        ],
    )
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
            logger.error(e)
            return Response({"message": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
