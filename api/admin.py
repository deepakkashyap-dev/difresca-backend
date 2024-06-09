from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from .models import Product,ProductGallery,HomepageBlock,Account,Banners,Category,Subcategory,Tag
from .forms import HomepageBlockAdminForm,ProductAdminForm
# Register your models here.
 
class GalleryInline(admin.StackedInline): 
    model = ProductGallery
    extra = 3
    fields = ['image','product']
    # template = 'admin/productgallery_inline.html'  

class ProductAdmin(admin.ModelAdmin):
    inlines = [GalleryInline]
    list_display=['name','section','quantity','price','is_active']
    # form = ProductAdminForm
    # class Media:
    #     js = ( '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', # jquery
    #           'admin/js/product_admin.js',
    #           )
  

# @admin.register(ProductGallery)
# class GalleryInline(admin.ModelAdmin):
#     pass

class Account_Table(admin.ModelAdmin):
    list_display=['username','name','email']

class Banner_Table(admin.ModelAdmin):
    list_display=['sequence','Banner_name','relation','is_active']

class Category_Table(admin.ModelAdmin):
    list_display=['name','slug']

class Subcategory_Table(admin.ModelAdmin):
    list_display=['name','slug','category']

class Tag_Table(admin.ModelAdmin):
    list_display=['name','slug']

class HomepageBlockAdmin(admin.ModelAdmin):
    form = HomepageBlockAdminForm
    list_display=['sequence','block_name','type','is_active']

admin.site.register(Product, ProductAdmin)
admin.site.register(HomepageBlock, HomepageBlockAdmin)
admin.site.register(Account, Account_Table)
admin.site.register(Banners, Banner_Table)
admin.site.register(Category, Category_Table)
admin.site.register(Subcategory, Subcategory_Table)
admin.site.register(Tag, Tag_Table)

app_models = apps.get_app_config('api').get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass

