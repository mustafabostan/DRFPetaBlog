from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Permission
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import CanAddBlog, IsAdminOrReadOnly, CanEditOrDeleteBlog, CanAddCategory, CanAddUser, CanEditOrDeleteUser, IsAdminUserOrOwner, CanEditOrDeleteCategory
from django.contrib.auth import get_user_model
from .models import Blog, Category
from .serializers import CustomTokenObtainPairSerializer, UserSerializer, UserPermissionSerializer, BlogSerializer, CategorySerializer

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



# Kullanici kayit islemi
class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    def post(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": UserSerializer(user).data,
                "message": "User created successfuly.",
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Kullanici listesi
class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]
    def get_serializer(self, *args, **kwargs):
        kwargs['fields'] = ('id', 'username', 'email', 'first_name', 'last_name')
        return UserSerializer(*args, **kwargs)


# Kullanici detayi
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_serializer(self, *args, **kwargs):
        kwargs['fields'] = ('id', 'username', 'email', 'first_name', 'last_name', 'phone_code', 'phone_number')
        return UserSerializer(*args, **kwargs)


# Kullanici guncelleme islemi
class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUserOrOwner]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Kullanici silme islemi
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUserOrOwner]
    lookup_field = 'id'

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "User deleted successfuly."}, status=status.HTTP_200_OK)




### Kullanici yetkileri ###

# Kullanici yetkileri listesi
class UserPermissionView(generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    lookup_field = 'id'
    serializer_class = UserPermissionSerializer
    permission_classes = [IsAdminUser]


    def get(self, request, *args, **kwargs):
        user = self.get_object()
        permissions = user.user_permissions.all()
        return Response({"permissions": [permission.codename for permission in permissions]}, status=status.HTTP_200_OK)
    

# Kullanici yetki ekleme-silme islemi
class UserPermissionUpdateView(generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserPermissionSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        permission_codename = request.data.get('permission')
        action = request.data.get('action')

        if not permission_codename or not action:
            return Response({"error": "Permission and action fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            permission = Permission.objects.get(codename=permission_codename)
        except Permission.DoesNotExist:
            return Response({"error": "Permission not found."}, status=status.HTTP_404_NOT_FOUND)

        if action == 'add':
            user.user_permissions.add(permission)
            message = "Permission added successfully."
        elif action == 'remove':
            user.user_permissions.remove(permission)
            message = "Permission removed successfully."
        else:
            return Response({"error": "Invalid action. Use 'add' or 'remove'."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": message}, status=status.HTTP_200_OK)




### Kategori islemleri ###

# Kateogri listeleme 
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

# Kategori ekleme
class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, CanAddCategory] 

# Kategori detayi, guncelleme ve silme
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, CanEditOrDeleteCategory]
    lookup_field = 'id'



### Blog islemleri ###


# Blog listeleme
class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated] 

# Blog ekleme
class BlogCreateView(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated, CanAddBlog]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            blog = serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Blog detayi
class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.filter(is_active=True)
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

# Blog guncelleme
class BlogUpdateView(generics.UpdateAPIView):
    queryset = Blog.objects.filter(is_active=True)
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated, CanEditOrDeleteBlog]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Blog silme
class BlogDeleteView(generics.DestroyAPIView):
    queryset = Blog.objects.filter(is_active=True)
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated, CanEditOrDeleteBlog]
    lookup_field = 'id'

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "blog deleted successfully."}, status=status.HTTP_200_OK)