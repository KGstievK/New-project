from django.contrib.auth.models import *
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
import uuid
from django.db.models.signals import post_delete
from django.dispatch import receiver
from datetime import datetime, timedelta
import os


def generate_unique_filename(filename):
    random_string = str(uuid.uuid4())[:10]
    return random_string + '_' + filename.replace(' ', '_')


class Basket(models.Model):
    title = models.CharField(max_length=50)

    def get_products(self):
        products = self.basket_products.all()
        basket_products = []
        for p in products:
            print(f'im: {p}')
            basket_products.append({
                'id': p.id,
                'name': p.name,
                'price': p.price,
                'images': p.get_image(),
                'rating': p.rating
            })
        return basket_products

    def __str__(self):
        return self.title


class Favorite(models.Model):
    title = models.CharField(max_length=50)

    def get_products(self):
        products = self.favorite_products.all()
        favorite_products = []
        for p in products:
            print(f'im: {p}')
            favorite_products.append({
                'id': p.id,
                'name': p.name,
                'price': p.price,
                'images': p.get_image(),
                'rating': p.rating
            })
        return favorite_products

    def __str__(self):
        return self.title


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Address(models.Model):
    city = models.CharField(max_length=100, null=True, blank=True)
    area = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    home = models.CharField(max_length=100, null=True, blank=True)
    flat = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'address id: {self.pk}, city: {self.city}'


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    last_login = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    address = models.ForeignKey(Address, verbose_name='user_address', on_delete=models.CASCADE, null=True, blank=True)

    basket = models.ForeignKey(Basket, verbose_name='user_basket', on_delete=models.CASCADE, null=True, blank=True)
    favorite = models.ForeignKey(Favorite, verbose_name='user_favorite', on_delete=models.CASCADE, null=True, blank=True)

    objects = UserManager()
    # username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Color(models.Model):
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'color'
        verbose_name_plural = 'colors'

    def __str__(self):
        return self.title


class Characteristic(models.Model):
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'characteristic'
        verbose_name_plural = 'characteristics'

    def __str__(self):
        return f'{self.title} {self.value}'


class Category(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_id(self):
        return self.pk

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Sub category'
        verbose_name_plural = 'Sub categories'

    def __str__(self):
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=50)
    logo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=10000)
    price = models.PositiveIntegerField(default=0)
    count = models.PositiveIntegerField(default=1)
    discount = models.PositiveIntegerField(null=True, blank=True)
    current_price = models.PositiveIntegerField(null=True, blank=True)
    economy = models.PositiveIntegerField(null=True, blank=True)
    rating = models.PositiveIntegerField(default=0, null=True, blank=True)
    in_stock = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    new = models.BooleanField(default=True, null=True, blank=True)
    brand = models.ForeignKey(Brand, verbose_name='brand', on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name='category', on_delete=models.CASCADE, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, verbose_name='sub_category', on_delete=models.CASCADE, null=True, blank=True)
    colors = models.ManyToManyField(Color, related_name="product_colors", blank=True)
    characteristics = models.ManyToManyField(Characteristic, related_name='pro_char', blank=True)
    baskets = models.ManyToManyField(Basket, related_name='basket_products', null=True, blank=True)
    favorites = models.ManyToManyField(Favorite, related_name='favorite_products', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.price is not None and self.discount is not None:
            self.current_price = self.price - (self.price * self.discount // 100)
            self.economy = self.price - self.current_price
        else:
            self.current_price = None
            self.economy = None
        super().save(*args, **kwargs)

    def get_image(self):
        images = self.image_set.all()
        url_images = []
        for i in images:
            url_images.append(i.image.url)
        return url_images

    def get_characteristic(self):
        characteristics = self.characteristics.all()
        characteristics2 = []
        for i in characteristics:
            characteristics2.append({
                'id': i.id,
                'title': i.title,
                'value': i.value
            })
        return characteristics2

    def get_review(self):
        reviews = self.reviews.all()
        reviews2 = []
        for r in reviews:
            print(f'review: {r.title}')
            reviews2.append({
                'id': r.pk,
                'title': r.title,
                'date': r.date,
                'user': {
                    'id': r.user.id,
                    'firstName': r.user.firstName,
                    'lastName': r.user.lastName
                },
                'parent_review': r.parent_review
            })

        return reviews2

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField()
    product = models.ForeignKey(Product, verbose_name="product", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.image.name = generate_unique_filename(self.image.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.image.name


@receiver(post_delete, sender=Image)
def delete_image_file(sender, instance, **kwargs):
    # Получаем количество продуктов, связанных с изображением
    products_count = Product.objects.filter(image=instance).count()

    # Если изображение больше не связано ни с одним продуктом, удаляем файл изображения
    if products_count == 0:
        if instance.image:
            if os.path.isfile(instance.image.path):
                os.remove(instance.image.path)


class Review(models.Model):
    title = models.TextField(max_length=1000)
    rating = models.PositiveIntegerField(default=0, null=True, blank=True)
    date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, related_name='rev_user', on_delete=models.CASCADE, null=True)
    parent_review = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='product', on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f'review id: {self.pk} | title: {self.title}'


