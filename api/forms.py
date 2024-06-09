from django import forms
from .models import HomepageBlock, ProductGallery,Product,Subcategory
from django.core.exceptions import ValidationError

class HomepageBlockAdminForm(forms.ModelForm):
    class Meta:
        model = HomepageBlock
        fields = '__all__'

    def clean_block_name(self):
        block_name = self.cleaned_data.get('block_name')
        if block_name and ' ' in block_name:
            raise ValidationError("Block name should not contain white spaces, u can use - or _ instead.")
        return block_name

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Access the request object from the kwargs
    #     request = kwargs.get('request')
    #     if request:
    #         # Filter subcategories based on the selected category
    #         if 'category' in request.POST:
    #             try:
    #                 category_id = int(request.POST.get('category'))
    #                 self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
    #                 self.initial['subcategory'] = self.instance.subcategory
    #             except (ValueError, TypeError):
    #                 pass
    #         elif self.instance.pk:
    #             # If editing an existing product, filter subcategories based on the current category
    #             self.fields['subcategory'].queryset = self.instance.category.subcategory_set.all()



























# class ProductAdminForm(forms.ModelForm):
#     image_file = forms.FileField(required=False, label='Upload product image')
#     class Meta:
#         model = Product
#         fields = '__all__'

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         image_file = self.cleaned_data.get('image_file')
#         if image_file:
#             instance.image_data = image_file.read()
#         if commit:
#             instance.save()
#         return instance


# class ProductGalleryAdminForm(forms.ModelForm):
#     image_file = forms.FileField(required=False, label='Upload gallery image')
#     class Meta:
#         model = ProductGallery
#         fields = '__all__'

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         image_file = self.cleaned_data.get('image_file')
#         if image_file:
#             instance.image_data = image_file.read()
#         if commit:
#             instance.save()
#         return instance
