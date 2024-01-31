# from django import forms
# from .models import ProductGallery,Product


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
