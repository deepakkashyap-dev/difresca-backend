from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from .models import Product,ProductGallery,HomepageBlock,Account,Banners
# from .forms import ProductAdminForm,ProductGalleryAdminForm

# Register your models here.
 
class GalleryInline(admin.StackedInline): 
    model = ProductGallery
    extra = 3
    fields = ['image','product']
    # template = 'admin/productgallery_inline.html'  

class ProductAdmin(admin.ModelAdmin):
    inlines = [GalleryInline]

    # class Meta:
    #     model=Product

# @admin.register(ProductGallery)
# class GalleryInline(admin.ModelAdmin):
#     pass

class Account_Table(admin.ModelAdmin):
    list_display=['username','name','email']

class HomepageBlock_Table(admin.ModelAdmin):
    list_display=['sequence','block_name','type','is_active']

class Banner_Table(admin.ModelAdmin):
    list_display=['sequence','Banner_name','relation','is_active']
admin.site.register(Product, ProductAdmin)
admin.site.register(HomepageBlock, HomepageBlock_Table)
admin.site.register(Account, Account_Table)
admin.site.register(Banners, Banner_Table)


app_models = apps.get_app_config('api').get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass

