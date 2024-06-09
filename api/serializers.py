from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import HomepageBlock,Banners,Product,Category,Subcategory,Tag,Account

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id','name','first_name','last_name','email','phone_number','date_of_birth','profile_picture','gender','city','state','postal_code']

    def to_representation(self, instance):
        # Call the parent class's to_representation method
        data = super().to_representation(instance)
        # Check if the profile_picture field is not empty
        if not instance.profile_picture:
            # Exclude the profile_picture field from the serialized data
            data.pop('profile_picture', None)
        return data
    
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

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields = [ "id",'name','slug']
        # fields='__all__'

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Subcategory
        fields = [ "id",'name','slug']
        # fields='__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tag
        fields=[ "id", "name",  "slug"]
    
class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategory = SubcategorySerializer()
    tags = TagSerializer(many=True)
    # section = HomepageBlockSerializer()
    section = serializers.SerializerMethodField()  

    class Meta:
        model=Product
        fields='__all__'
        
    def get_section(self, obj):
        return obj.section.block_name if obj.section else None