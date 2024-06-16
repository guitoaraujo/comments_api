from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, TagViewSet

router = DefaultRouter()
router.register(r'comments', CommentViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
	path('', include(router.urls)),
	path('comments/<int:comment_id>/tags/', CommentViewSet.as_view({'post': 'tags', 'get': 'tags'}), name='comment-tags'),
	path('comments/pandas_data/', CommentViewSet.as_view({'get': 'pandas_data'}), name='pandas-data'),
]