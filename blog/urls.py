from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import  CustomTokenObtainPairView, RegisterView, UserListView, UserDetailView, UserUpdateView, UserDeleteView ,UserPermissionView, UserPermissionUpdateView, CategoryListView, CategoryCreateView, CategoryDetailView, BlogListView, BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView 
urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create/kullanici/', RegisterView.as_view(), name='auth_register'),
    path('get/kullanici-listesi', UserListView.as_view(), name='user_list'),
    path('get/kullanici/<int:id>/', UserDetailView.as_view(), name='user_detail'),
    path('update/kullanici/<int:id>/', UserUpdateView.as_view(), name='user_update'),
    path('delete/kullanici/<int:id>/', UserDeleteView.as_view(), name='user_delete'),
    path('get/kullanici-yetkileri/<int:id>/', UserPermissionView.as_view(), name='user_permission_detail'),
    path('update/kullanici-yetkileri/<int:id>/', UserPermissionUpdateView.as_view(), name='user_permission_update'),
    path('get/blog-kategorileri/', CategoryListView.as_view(), name='category_list'),
    path('create/kategori/', CategoryCreateView.as_view(), name='category_create'),
    path('get/kategori/<int:id>/', CategoryDetailView.as_view(), name='category_detail'),
    path('get/blog-listesi/', BlogListView.as_view(), name='blog_list'),
    path('create/blog/', BlogCreateView.as_view(), name='blog_create'),
    path('get/blog/<int:id>/', BlogDetailView.as_view(), name='blog_detail'),
    path('update/blog/<int:id>/', BlogUpdateView.as_view(), name='blog_update'),
    path('delete/blog/<int:id>/', BlogDeleteView.as_view(), name='blog_delete'),
]