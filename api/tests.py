from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Comment, Tag
from .serializers import TagSerializer
from unittest.mock import patch

class CommentViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.comment = Comment.objects.create(text="This is a test comment")
        self.tag = Tag.objects.create(name="test_tag")
        self.comment.tags.add(self.tag)
        self.valid_tag_payload = {'tag': 'new_tag'}
        self.invalid_tag_payload = {'tag': ''}

    def test_get_tags(self):
        url = reverse('comment-tags', kwargs={'pk': self.comment.pk})
        response = self.client.get(url)
        tags = self.comment.tags.all()
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    @patch('api.views.test_task.delay')
    def test_add_tag(self, mock_test_task_delay):
        url = reverse('comment-tags', kwargs={'pk': self.comment.pk})

        # Test valid tag addition
        response = self.client.post(url, self.valid_tag_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Tag added successfully.')
        self.assertTrue(Tag.objects.filter(name='new_tag').exists())
        mock_test_task_delay.assert_called_once()

        # Test invalid tag addition
        response = self.client.post(url, self.invalid_tag_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Tag name is required.')

    def tearDown(self):
        self.comment.delete()
        self.tag.delete()

