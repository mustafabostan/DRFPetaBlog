from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Blog, Category
from django.contrib.auth.models import Permission

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token    


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'password', 'password2', 'email', 'phone_code', 'phone_number')
        read_only_fields = ('id',)

    def __init__(self, *args, **kwargs):
        # Dinamik alanları desteklemek için fields parametresini alıyoruz
        fields = kwargs.pop('fields', None)
        super(UserSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Belirtilen alanların dışında kalanları kaldırıyoruz
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def validate(self, attrs):
        # Şifrelerin aynı olup olmadığını kontrol ediyoruz
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        # password2 alanını validated_data'dan kaldırıyoruz çünkü User modelinde bu alan bulunmuyor
        validated_data.pop('password2')
        # Yeni kullanıcı oluşturuyoruz ve şifreyi set_password ile belirliyoruz
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        # password2 alanını validated_data'dan kaldırıyoruz çünkü User modelinde bu alan bulunmuyor
        validated_data.pop('password2', None)

        # instance'da ki mevcut bilgileri validated_data ile güncelliyoruz
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        
        instance.save()
        return instance
    
class UserPermissionSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(
        many = True,
        slug_field = 'codename',
        queryset = Permission.objects.all(),
        source = 'user_permissions'
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'is_superuser', 'is_staff', 'is_active', 'permissions')
        read_only_fields = ('id', 'username', 'is_superuser', 'is_staff', 'is_active')

    def update(self, instance, validated_data):
        permissions = validated_data.pop('user_permissions', None)

        instance = super().update(instance, validated_data)

        if permissions is not None:
            instance.user_permissions.clear()
            for permission in permissions:
                instance.user_permissions.add(permission)
        
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
    
    def create(self, validated_data):
        blog = Blog(**validated_data)
        blog.save()
        return blog

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    
