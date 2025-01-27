from rest_framework import serializers
from .models import *


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializers(serializers.ModelSerializer):
    category = CategorySerializers()
    class Meta:
        model = SubCategory
        fields = ['id', 'title', 'category']


class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ColorsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class CharacterSerializers(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = '__all__'


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

