from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from .models import HomepageBlock,Banners,Product
from .serializers import ChangePasswordSerializer,HomepageBlockSerializer,BannerSerializer,ProductListSerializer
import json

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
    queryset = HomepageBlock.objects.filter(is_active=True)
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
            return Response(serializer.data)
        # elif regular_dict['type'] == 'STICKY_NOTES':

          

        # elif pk == 'table2':
        #     queryset = Model2.objects.all()
        #     serializer = Model2Serializer(queryset, many=True)
        # else:
        #     return Response({'error': 'Invalid pa+rameter'}, status=status.HTTP_400_BAD_REQUEST)

        # if serializer.is_valid():
        #     return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListView(generics.ListAPIView):
    permission_classes=[AllowAny]
    # queryset = Product.objects.filter(is_active=True,type='PRODUCT')
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductListSerializer