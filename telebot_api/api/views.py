from django.contrib.auth import get_user_model

from post.models import Post
from rest_framework import viewsets

from .permissions import UpdateOnlyAdminOrAuthor
from .serializers import PostSerializer

User = get_user_model()

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [UpdateOnlyAdminOrAuthor]
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
