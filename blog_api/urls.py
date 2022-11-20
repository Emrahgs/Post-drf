from django.urls import path
from .views import *
# from .views import PostList
# from rest_framework.routers import DefaultRouter

app_name = 'blog_api'

# router = DefaultRouter()
# router.register('', PostList, basename='post')
# urlpatterns = router.urls

urlpatterns = [
    path('posts/<int:pk>/', PostDetail.as_view(), name='detailcreate'),
    path('search/', PostListDetailfilter.as_view(), name='postsearch'),
    path('admin/create/', CreatePost.as_view(), name='createpost'),
    path('', PostList.as_view(), name='listcreate')
]
