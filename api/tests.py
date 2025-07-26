from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Contact, Label


class ContactAPITest(APITestCase):
    """API 테스트"""

    def setUp(self):
        self.client = APIClient()

        self.contact1 = Contact.objects.create(
            name='홍길동',
            email='hong@example.com',
            phone='010-1234-5678',
            company='A회사',
            memo='수영을 좋아함',
            website='http://www.honggil.dong'
        )
        self.contact1.labels.add(Label.objects.create(name='개발자'))
        self.contact1.labels.add(Label.objects.create(name='친구'))
        
        self.contact2 = Contact.objects.create(
            name='김철수',
            email='kim@example.com',
            phone='010-9876-5432',
            company='B회사'
        )
        
    def test_contact_list(self):
        """연락처 리스트 조회"""
        url = '/api/contacts/'  # URL 패턴에 맞게 수정
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']) , 2)
        self.assertNotIn('memo', response.data['results'][0])

    def test_contact_create(self):
        """연락처 생성"""
        url = '/api/contacts/'
        contact_data = {
            'name': '이영희',
            'email': 'lee@example.com',
            'phone': '010-5555-6666',
            'company': '테스트 회사',
            'job_title': '디자이너',
            'label_names': ['친구', '디자이너']
        }
        response = self.client.post(url, contact_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        contact = Contact.objects.get(id=response.data['id'])
        self.assertEqual(contact.name, '이영희')
        self.assertEqual(contact.email, 'lee@example.com')
        self.assertEqual(contact.phone, '010-5555-6666')
        self.assertEqual(contact.company, '테스트 회사')
        self.assertEqual(contact.job_title, '디자이너')
        self.assertEqual(contact.labels.count(), 2)

    def test_contact_create_fail(self):
        """연락처 생성 실패"""
        url = '/api/contacts/'
        invalid_data = {
            'email': 'invalid-email',  # 잘못된 이메일 형식
            'phone': '010-1234-5678'
        }

        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_contact_detail(self):
        """연락처 상세 조회"""
        url = f'/api/contacts/{self.contact1.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], '홍길동')
        self.assertEqual(response.data['email'], 'hong@example.com')
        self.assertEqual(response.data['website'], 'http://www.honggil.dong')
        self.assertEqual(len(response.data['labels']), 2)

    def test_contact_update(self):
        """연락처 수정 """
        url = f'/api/contacts/{self.contact1.id}/'
        update_data = {
            'name': '홍길동 수정',
            'company': '수정된 회사',
            'job_title': '수정된 직책',
        }

        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_contact = Contact.objects.get(id=self.contact1.id)
        self.assertEqual(updated_contact.name, '홍길동 수정')
        self.assertEqual(updated_contact.company, '수정된 회사')
        self.assertEqual(updated_contact.job_title, '수정된 직책')