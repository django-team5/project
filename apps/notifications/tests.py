from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Notification
from .serializers import NotificationSerializer
from .logic import create_notification, get_notification_message, trigger_notification

User = get_user_model()

class NotificationModelTest(TestCase):
    """Notification 모델 테스트"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
    
    def test_notification_creation(self):
        """알림 생성 테스트"""
        notification = Notification.objects.create(
            user=self.user,
            message='테스트 알림',
            type='comment'
        )
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.message, '테스트 알림')
        self.assertEqual(notification.type, 'comment')
        self.assertFalse(notification.is_read)
        self.assertTrue(notification.created_at)
    
    def test_notification_str_method(self):
        """알림 __str__ 메서드 테스트"""
        notification = Notification.objects.create(
            user=self.user,
            message='테스트 알림',
            type='general'
        )
        expected = f'[{self.user}] 테스트 알림'
        self.assertEqual(str(notification), expected)
    
    def test_notification_default_values(self):
        """알림 기본값 테스트"""
        notification = Notification.objects.create(
            user=self.user,
            message='기본값 테스트'
        )
        self.assertEqual(notification.type, 'general')
        self.assertFalse(notification.is_read)

class NotificationSerializerTest(TestCase):
    """Notification 시리얼라이저 테스트"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.notification = Notification.objects.create(
            user=self.user,
            message='테스트 알림',
            type='comment'
        )
    
    def test_serializer_data(self):
        """시리얼라이저 데이터 검증"""
        serializer = NotificationSerializer(self.notification)
        data = serializer.data
        self.assertEqual(data['user'], self.user.id)
        self.assertEqual(data['message'], '테스트 알림')
        self.assertEqual(data['type'], 'comment')
        self.assertFalse(data['is_read'])

class NotificationLogicTest(TestCase):
    """Notification 로직 테스트"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_notification_function(self):
        """알림 생성 함수 테스트"""
        notification = create_notification(
            user=self.user,
            message='로직 테스트',
            notif_type='like'
        )
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.message, '로직 테스트')
        self.assertEqual(notification.type, 'like')
    
    def test_get_notification_message(self):
        """알림 메시지 생성 함수 테스트"""
        comment_msg = get_notification_message('comment', username='테스터')
        like_msg = get_notification_message('like', username='좋아요유저')
        general_msg = get_notification_message('general', message='일반 알림')
        
        self.assertEqual(comment_msg, '테스터님이 댓글을 남겼습니다.')
        self.assertEqual(like_msg, '좋아요유저님이 좋아요를 눌렀습니다.')
        self.assertEqual(general_msg, '일반 알림')
    
    def test_trigger_notification(self):
        """알림 트리거 함수 테스트"""
        notification = trigger_notification(
            event_type='comment',
            user=self.user,
            username='댓글작성자'
        )
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.type, 'comment')
        self.assertIn('댓글작성자님이 댓글을', notification.message)

class NotificationAPITest(APITestCase):
    """Notification API 테스트"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            email='other@example.com',
            password='testpass123'
        )
        self.notification1 = Notification.objects.create(
            user=self.user,
            message='첫 번째 알림',
            type='comment'
        )
        self.notification2 = Notification.objects.create(
            user=self.user,
            message='두 번째 알림',
            type='like',
            is_read=True
        )
        self.other_notification = Notification.objects.create(
            user=self.other_user,
            message='다른 사용자 알림',
            type='general'
        )
        self.list_url = reverse('notification-list')
        self.detail_url = reverse('notification-detail', kwargs={'pk': self.notification1.pk})
        self.bulk_read_url = reverse('notification-bulk-read')
    
    def test_get_notifications_authenticated(self):
        """인증된 사용자의 알림 조회 테스트"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)  # 본인 알림만 조회
    
    def test_get_notifications_unauthenticated(self):
        """비인증 사용자의 알림 조회 테스트"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_filter_unread_notifications(self):
        """읽지 않은 알림만 필터링 테스트"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url + '?unread=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)  # 읽지 않은 알림만
    
    def test_filter_notifications_by_type(self):
        """알림 타입별 필터링 테스트"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url + '?type=comment')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_notification_detail_view(self):
        """단일 알림 조회 테스트"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], '첫 번째 알림')
    
    def test_mark_notification_as_read(self):
        """알림 읽음 처리 테스트"""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification1.refresh_from_db()
        self.assertTrue(self.notification1.is_read)
    
    def test_delete_notification(self):
        """알림 삭제 테스트"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Notification.objects.filter(pk=self.notification1.pk).exists())
    
    def test_bulk_mark_as_read(self):
        """알림 일괄 읽음 처리 테스트"""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.bulk_read_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['updated'], 1)  # 읽지 않은 알림 1개 업데이트
        
        self.notification1.refresh_from_db()
        self.assertTrue(self.notification1.is_read)
    
    def test_user_cannot_access_other_notifications(self):
        """다른 사용자의 알림 접근 불가 테스트"""
        self.client.force_authenticate(user=self.user)
        other_detail_url = reverse('notification-detail', kwargs={'pk': self.other_notification.pk})
        response = self.client.get(other_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_pagination(self):
        """페이징 테스트"""
        # 추가 알림 생성
        for i in range(15):
            Notification.objects.create(
                user=self.user,
                message=f'알림 {i}',
                type='general'
            )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # 페이지 크기 10
        self.assertIsNotNone(response.data['next'])  # 다음 페이지 존재 