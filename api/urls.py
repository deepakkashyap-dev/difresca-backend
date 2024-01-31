from django.urls import path,include
from . import views 

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    #Auth
    path('signup', views.SignupView.as_view()),
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('change_password', views.change_password, name='change_password'),
    path('password_reset', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # Homepage
    path('homepage/all', views.HomepageListView.as_view(), name='home_page_block'),
    path('homepage/blocks/<int:pk>', views.HomeDetailView.as_view(), name='home_block_data'),
    path('product/all', views.ProductListView.as_view(), name='home_block_data'),

]