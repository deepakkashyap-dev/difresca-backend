from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.text import slugify


class MyAccountManager(BaseUserManager):  # Custom user model manager where email is the unique identifiers for authentication instead of usernames.
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            return ValueError("Users must have an email address")
        if not name:
            return ValueError("Users must have a name")
        user = self.model(email=self.normalize_email(
            email),  name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        user = self.create_user(
            email=email, password=password,  name=name, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_admin(self, email, name, password=None, **extra_fields):
        user = self.create_user(email=self.normalize_email(
            email),  password=password,  name=name, **extra_fields)
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class Account(AbstractUser, PermissionsMixin):  # Custom user model where email is the unique identifiers for authentication instead of usernames.
    username = models.CharField(max_length=100, unique=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(
        verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)
    phone_number = models.CharField(
        max_length=15, blank=True, null=True, unique=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=25, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    is_email_validate = models.BooleanField(default=False)
    is_phone_validate = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = MyAccountManager()

    def __str__(self):
        return self.email

class Address(models.Model):    # Address model for user
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    addr_phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)

class Tag(models.Model): # Tag model for product
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, unique=True, editable=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["slug"]
        verbose_name = "tag"

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

class Category(models.Model): # Category model for product
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, editable=False)
    category_image = models.ImageField(
        upload_to='images/category/main/', blank=True, default='category_image.jpg')
    thumbnail = models.ImageField(
        upload_to='images/category/thumbnails/', blank=True, editable=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        if not self.category_image:
            original_image = Image.open(self.category_image)
            thumbnail_size = (100, 100)  # Adjust the size as needed
            original_image.thumbnail(thumbnail_size)
            thumbnail_buffer = BytesIO()
            format = original_image.format  # Get the original format
            original_image.save(thumbnail_buffer, format=format)
            thumbnail_file = InMemoryUploadedFile(
                thumbnail_buffer,
                None,  # Field name (not needed here)
                # File name
                f'{self.category_image.name.split("/")[-1].split(".")[0]}_thumbnail.{format.lower()}',
                f'image/{format.lower()}',  # Content type
                thumbnail_buffer.tell,  # File size
                None  # Content type extra headers
            )
            # Save the thumbnail to the model's thumbnail_image field
            self.thumbnail.save(thumbnail_file.name, thumbnail_file)
            # Save the model again to store the thumbnail_image field
            super().save(*args, **kwargs)

class Subcategory(models.Model): # Subcategory model for product
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
   
class Product(models.Model): # Product model
    name = models.CharField(max_length=255) 
    slug = models.CharField(max_length=255, editable=False)
    description = models.TextField()
    tags = models.ManyToManyField(Tag)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=255, default='1 each')
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    sale_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    max_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    min_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    product_image = models.ImageField(
        upload_to='images/product/main/', default='')
    thumbnail = models.ImageField(
        upload_to='images/product/thumbnails/', blank=True, editable=False)
    # gallery_images = models.ManyToManyField('ProductGallery', blank=True,null=True,related_name='products') #,related_name='products'
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        if not self.product_image:
            img = Image.open(self.product_image)
            thumbnail_size = (100, 100)
            img.thumbnail(thumbnail_size)
            thumb_io = BytesIO()
            format = img.format
            img.save(thumb_io, format=format)
            thumbnail_file = InMemoryUploadedFile(
                thumb_io,
                None,  # Field name (not needed here)
                # File name
                f'{self.product_image.name.split("/")[-1].split(".")[0]}_thumbnail.{format.lower()}',
                f'image/{format.lower()}',  # Content type
                thumb_io.tell,  # File size
                None  # Content type extra headers
            )
            self.thumbnail.save(thumbnail_file.name, thumbnail_file)
            super().save(*args, **kwargs)
            thumb_io.close()

class ProductGallery(models.Model): # Product gallery model
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True,
                                related_name='gallery_images', default='')  # , null=True,related_name='images'
    image = models.ImageField(upload_to='images/gallery/main/')
    thumbnail = models.ImageField(
        upload_to='images/gallery/thumbnails/', blank=True, editable=False)

    def __str__(self):
        return self.image.name

    # def __str__(self):
    #     return f"Image for {self.product.name}"

    def save(self, *args, **kwargs):
        if not self.image:
            img = Image.open(self.image)
            thumbnail_size = (100, 100)
            img.thumbnail(thumbnail_size)
            thumb_io = BytesIO()
            format = img.format
            img.save(thumb_io, format=format)
            thumbnail_file = InMemoryUploadedFile(
                thumb_io,
                None,  # Field name (not needed here)
                # File name
                f'{self.image.name.split("/")[-1].split(".")[0]}_thumbnail.{format.lower()}',
                f'image/{format.lower()}',  # Content type
                thumb_io.tell,  # File size
                None  # Content type extra headers
            )
            self.thumbnail.save(thumbnail_file.name, thumbnail_file)
            super().save(*args, **kwargs)
            thumb_io.close()

class Order(models.Model): # Order model
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[(
        'Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')])

class OrderItem(models.Model): ## Order item model
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

HOME_PAGE_BLOCK_TYPE = (
        ("HERO_IMAGE", "HERO_IMAGE"),
        ("CATEGORY_PRODUCT", "CATEGORY_PRODUCT"),
        ("STICKY_NOTES", "STICKY_NOTES"),
        # ("BRAND_BANNER", "BRAND_BANNER"),
)
def no_whitespace_validator(value): # validator for homepage block name
    if ' ' in value:
        raise models.ValidationError("Spaces are not allowed in this field.")

class HomepageBlock(models.Model): # Homepage block model
    type = models.CharField(max_length = 255, choices = HOME_PAGE_BLOCK_TYPE)
    heading = models.CharField(max_length=255, blank=True, null=True)
    sub_Heading = models.CharField(max_length=255, blank=True, null=True)
    block_name = models.CharField(max_length=255,validators=[no_whitespace_validator],blank=False)
    sequence = models.IntegerField(blank=False,unique=True)
    is_active = models.BooleanField(default=True)
    slider =  models.BooleanField(default=False)
    product_count = models.IntegerField(default=0)
    Card_In_A_Row = models.CharField( max_length=100, blank=True, null=True, default=None )
    def __str__(self):
        return f"{self.block_name}"
    
class Banners(models.Model): # Banner model
    WIDTH_CHOICE = (  ("3", "25 %"),  ("6", "50 %"),   ("9", "75 %"),  ("12", "full") ) 
    Banner_name =  models.CharField(max_length=100,null=True,blank=True)
    Banner_image = models.ImageField(upload_to='images/banner/', default='')
    button_text = models.CharField(max_length=100,null=True,blank=True)
    button_URL = models.CharField(max_length=100,null=True,blank=True)
    button_text_color = models.CharField(max_length=100,null=True,blank=True) 
    button_text_color_hover = models.CharField(max_length=100,null=True,blank=True) 
    button_background = models.CharField(max_length=100,null=True,blank=True)
    button_background_hover = models.CharField(max_length=100,null=True,blank=True)
    width = models.CharField(max_length=100,choices = WIDTH_CHOICE, default="12")
    relation = models.ForeignKey(HomepageBlock, on_delete=models.CASCADE,null=True)
    sequence = models.IntegerField(blank=False,unique=True,null=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.Banner_name}, width:{self.width}, {self.relation} , active:{self.is_active} "