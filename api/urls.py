from django.urls import path,include
from . import views 

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    #admin-panel
    path('subcategory', views.get_subcategories, name='get_subcategories'), #?category=${selectedCategoryId}
    #Auth
    path('signup', views.SignupView.as_view()),
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('token/user', views.UserProfileView.as_view(), name='user_profile'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('change_password', views.change_password, name='change_password'),
    path('password_reset', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # Homepage
    path('homepage/all', views.HomepageListView.as_view(), name='home_page_block'),
    path('homepage/block/<int:pk>', views.HomeDetailView.as_view(), name='home_block_data'),
    path('products/', views.ProductListView.as_view(), name='get_all_products'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='get_product_detail'),
    path('product/search', views.ProductSearchView.as_view(), name='search_products'),

]