from rest_framework import serializers
from post.models import Post
from rest_framework.exceptions import ValidationError


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(
        source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'pub_date', 'author_username']
        read_only_fields = ['id', 'pub_date', 'author_username']

    def create(self, validated_data):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            raise ValidationError("Пройдите авторизацию")
        validated_data['author'] = request.user
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            raise ValidationError("Пройдите авторизацию")
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.author = request.user
        instance.save()
        return instance
