from rest_framework import serializers
from .models import Comment, Tag

class TagSerializer(serializers.ModelSerializer):
	comments = serializers.SerializerMethodField()
	class Meta:
		model = Tag
		fields = ('id', 'name', 'comments')

	def get_comments(self, obj):
		return [{"id": comment.id, "text": comment.text} for comment in obj.comments.all()]

class CommentSerializer(serializers.ModelSerializer):
	tags = serializers.SerializerMethodField()

	class Meta:
		model = Comment
		fields = ('id', 'text', 'tags', 'created_at')

	def get_tags(self, obj):
		return [{"id": tag.id, "name": tag.name} for tag in obj.tags.all()]




