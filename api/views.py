import pandas as pd
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Comment, Tag
from .serializers import CommentSerializer, TagSerializer
from .filters import TagFilterBackend
from .tasks import test_task

class CommentViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	filter_backends = [filters.SearchFilter, TagFilterBackend]
	search_fields = ['text', 'tags__name']

	@action(detail=True, methods=['get', 'post'])
	def tags(self, request, pk=None):	
		comment = self.get_object()

		if request.method == 'GET':
			tags = comment.tags.all()
			serializer = TagSerializer(tags, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		
		elif request.method == 'POST':
			tag_name = request.data.get('tag')
			if not tag_name:
				return Response({"detail": "Tag name is required."}, status=status.HTTP_400_BAD_REQUEST)

			tag, created = Tag.objects.get_or_create(name=tag_name)
			comment.tags.add(tag)
			comment.save()
			if created:
				subject = "Nova Tag Criada"
				message = f"A nova tag '{tag_name}' foi criada e adicionada ao comentário."
				from_email = "system@api.com"
				recipient_list = ["admin@api.com"]
				test_task.delay(subject, message, from_email, recipient_list)

			return Response({"detail": "Tag added successfully."}, status=status.HTTP_200_OK)

	@action(detail=False, methods=['get'])
	def pandas_data(self, request):
		comments = Comment.objects.all()
		serializer = CommentSerializer(comments, many=True)
		df = pd.DataFrame(serializer.data)
		df['num_tags'] = df['tags'].apply(lambda x: len(x))
		df_sorted = df.sort_values(by='num_tags', ascending=False)
		data_json = df_sorted.to_json(orient='records')

		return Response(data_json)

class TagViewSet(viewsets.ModelViewSet):
	queryset = Tag.objects.all()
	serializer_class = TagSerializer
