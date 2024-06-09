from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from .models import HomepageBlock,Banners,Product
from .serializers import ChangePasswordSerializer,HomepageBlockSerializer,BannerSerializer,ProductListSerializer,UserProfileSerializer,Subcategory
import json
from django.http import JsonResponse
from django.db.models import Q
import functools

User = get_user_model()

class SignupView(APIView):
    permission_classes = (AllowAny, )
    def post(self, request):
        try:
            data = request.data
            name = data['name']
            first_name = data['first_name']
            last_name = data['last_name']
            phone_number = data['phone_number']
            email = data['email'].lower()
            password = data['password']
            if len(password) >= 8:
                if not User.objects.filter(email=email).exists():
                    try:
                        user = User.objects.create_user(
                            name=name, email=email, first_name=first_name, password=password, last_name=last_name, phone_number=phone_number)
                        user.set_password(password)
                        user.save()
                        return Response(
                            {'success': 'User created Sucessfully.'},
                            status=status.HTTP_201_CREATED
                        )
                    except Exception as er:
                        print("Exception", er)
                else:
                    return Response(
                        {'error': 'User with this email is already exists.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {'error': 'Password must be at least 8 characters.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                {'error': 'Something went wrong while signup.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = request.user  # Assuming you have a UserProfile model linked to the User model
        # print(user_profile.name)
        serializer = UserProfileSerializer(user_profile)
        print(serializer.data)
        return Response(serializer.data)
    

    # def get(self, request):
    #     user = request.user
    #     # Customize the response data as needed
    #     data = {
    #         'id': user.id,
    #         'username': user.username,
    #         'name': user.name,
    #         'email': user.email,
    #         'phone': user.phone_number,
    #         'profile_image': user.profile_picture,
    #         "dob":  user.date_of_birth,
    #         'gender': user.gender,
    #         'city': user.city,
    #         'state': user.state,
    #         'postal_code': user.postal_code,
    #         # Add other user fields you want to include
    #     }
    #     return Response(data)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                # update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HomepageListView(generics.ListAPIView):
    permission_classes=[AllowAny]
    queryset = HomepageBlock.objects.filter(is_active=True).order_by('sequence')
    serializer_class = HomepageBlockSerializer

class HomeDetailView(APIView):
    permission_classes=[AllowAny]
    def get(self, request,  pk):
        data = HomepageBlock.objects.filter(pk=pk)
        block_serializer = HomepageBlockSerializer(data, many=True)
        regular_dict = dict(block_serializer.data[0])
        if (regular_dict['type'] == 'HERO_IMAGE' or regular_dict['type'] == 'STICKY_NOTES'):
            queryset = Banners.objects.filter(is_active=True,relation__block_name=regular_dict['block_name'])
            serializer = BannerSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # elif regular_dict['type'] == 'STICKY_NOTES':

        elif regular_dict['type'] == 'CATEGORY_PRODUCT':
            queryset = Product.objects.filter(is_active=True,section=pk)
            serializer = ProductListSerializer(queryset, many=True)
            return Response(serializer.data)
       
        # else:
        #     return Response({'error': 'Invalid parameter'}, status=status.HTTP_400_BAD_REQUEST)

        # if serializer.is_valid():
        #     return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListView(generics.ListAPIView):
    permission_classes=[AllowAny]
    serializer_class = ProductListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        block = self.request.query_params.get('block', None)
        head = {}
        all_tags = set()
        suggestion_products = []

        if block is not None:
            block_data = HomepageBlock.objects.filter(block_name=block).first()
            if block_data:
                head = {
                    'heading': block_data.heading,
                    'sub_heading': block_data.sub_Heading
                }
                queryset = queryset.filter(section__block_name=block)
                for product in queryset:  # get all tags from the filtered products for suggestions
                    all_tags.update(product.tags.values_list('slug', flat=True))

                # Exclude suggestion products from the filtered queryset
                suggestion_products = Product.objects.filter(tags__name__in=all_tags).distinct()
                unique_suggestion_products = suggestion_products.exclude(id__in=[product.id for product in queryset])

                    
        serializer = self.get_serializer(queryset, many=True)
        suggestion_serializer = self.get_serializer(unique_suggestion_products, many=True)
    
        data = {
            'products': serializer.data,
            'head': head,
            'tags': list(all_tags),
            'suggestion_products':suggestion_serializer.data
        }   
        return Response(data, status=status.HTTP_200_OK)
    def get_queryset(self):
        return Product.objects.all()

   
class ProductDetailView(generics.RetrieveAPIView):
    permission_classes=[AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    lookup_field = 'pk' 

def get_subcategories(request): # rerturn subcategories based on category dynamically
    category_id = request.GET.get('category')
    if category_id:
        subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
        return JsonResponse(list(subcategories), safe=False)
    else:
        return JsonResponse([], safe=False)
    
class ProductSearchView(generics.ListAPIView):
    permission_classes=[AllowAny]
    serializer_class = ProductListSerializer
    def get_queryset(self):
        queryset = Product.objects.all()
        keyword = self.request.data.get('keyword', '')
        if keyword:
            name_results = queryset.filter(slug__startswith=keyword)# get products starting with the keyword
            remaining_results = queryset.exclude(pk__in=name_results.values_list('pk', flat=True))

            # Combine query conditions for searching across multiple fields
            query = Q(slug__icontains=keyword) | \
                    Q(tags__name__contains=keyword) | \
                    Q(category__name__icontains=keyword) | \
                    Q(subcategory__name__icontains=keyword) | \
                    Q(description__icontains=keyword)

            # Search for products using combined query conditions
            other_fields_results = remaining_results.filter(query)[:5]
            results = name_results.union(other_fields_results)[:10]
            return results
        return Product.objects.none()
    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if queryset:
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No products found'},status=status.HTTP_200_OK)