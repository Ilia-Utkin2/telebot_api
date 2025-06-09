from post.models import Post
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(
        source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'pub_date', 'author_username']
        read_only_fields = ['id', 'pub_date', 'author_username']
        extra_kwargs = {
            'title': {'error_messages': {'required': 'Поле заголовка обязательно.'}},
            'text': {'error_messages': {'required': 'Поле текста обязательно.'}},
        }

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
        if instance.author != request.user and not (request.user.is_staff or request.user.is_superuser):
            raise ValidationError("Вы можете редактировать только свои посты.")
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance
