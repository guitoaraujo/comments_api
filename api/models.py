from django.db import models

class Comment(models.Model):
	text = models.TextField(max_length=150)
	tags = models.ManyToManyField('Tag', related_name='comments')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.text		

class Tag(models.Model):
	name = models.CharField(max_length=50, unique=True)

	def __str__(self):
		return self.name
