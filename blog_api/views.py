from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, filters, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticated
from blog.models import Post
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404

# Display Posts
class PostUserWritePermission(BasePermission):
    message = 'Editing posts is restricted to the author only.'

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user


# class PostList(viewsets.ModelViewSet):
#     permissions_classes = [PostUserWritePermission]
#     serializer_class = PostSerializer
#     queryset = Post.postobjects.all()
    
#     def get_object(self, queryset=None, **kwargs):
#         item = self.kwargs.get('pk')
#         return get_object_or_404(Post, slug=item)
    
#     # define custom queryset
#     def get_queryset(self):
#         return Post.objects.all()


# class PostList(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = Post.postobjects.all()
    
#     def list(self, request):
#         serializer_class = PostSerializer(self.queryset, many=True)
#         return Response(serializer_class.data)
    
#     def retrieve(self, request, pk=None):
#         post = get_object_or_404(self.queryset, pk=pk)
#         serializer_class = PostSerializer(post)
#         return Response(serializer_class.data)


class PostList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    
    def get_object(self):
        item = self.kwargs.get('pk')
        return get_object_or_404(Post, slug=item)
    
# Post Search
class PostListDetailfilter(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^slug']


class CreatePost(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
