from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Post, Like
from .serializer import (
    RegisterSerializer, UserSerializer,
    PostSerializer, LikeSerializer
)


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully. Login to get your token",
        })


class PostCreateApi(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostApi(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostUpdateApi(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDeleteApi(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class LikeCreateApi(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def create(self, request, *args, **kwargs):
        if like_obj := Like.objects.filter(
            value=(1 - request.data['value']),
            post_id=request.data["post"],
            user=request.user
        ):
            like_obj.delete()

        return super(LikeCreateApi, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeDeleteApi(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class LikeApi(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Like.objects.all()
    serializer_class = LikeSerializer
