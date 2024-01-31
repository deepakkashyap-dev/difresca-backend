from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import HomepageBlock,Banners,Product

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class HomepageBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model=HomepageBlock
        fields='__all__'

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Banners
        fields='__all__'
    
class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'
