from rest_framework import serializers
from .models import *


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'firstName', 'lastName', 'phone_number', 'password', 'image', 'address']
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)

        # Обновляем данные пользователя
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)

        instance.save()

        # Если адресные данные предоставлены и пользователь уже имеет адрес
        if address_data and instance.address:
            address = instance.address
            for attr, value in address_data.items():
                setattr(address, attr, value)
            address.save()
        # Если адресные данные предоставлены, но пользователь еще не имеет адреса
        elif address_data:
            address = Address.objects.create(**address_data)
            instance.address = address  # Присваиваем адрес пользователю
            instance.save()

        return instance


class UserSerializerForReview(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'firstName', 'lastName']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializerForReview()

    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    characteristics = serializers.SerializerMethodField()
    # characteristics = CharacteristicSerializer(many=True)
    category = CategorySerializer()
    sub_category = SubCategorySerializer()
    brand = BrandSerializer()
    colors = ColorSerializer(many=True)
    # review = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True)

    def get_images(self, obj):
        image_instances = obj.get_image()
        return image_instances

    def get_characteristics(self, obj):
        characteristic_instances = obj.get_characteristic()
        return characteristic_instances

    # def get_review(self, obj):
    #     review_instances = obj.get_review()
    #     return review_instances

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'count', 'discount', 'current_price', 'economy', 'rating',
                  'in_stock', 'date', 'new', 'brand', 'category', 'sub_category', 'colors', 'images', 'characteristics', 'reviews']


class BasketSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    def get_products(self, obj):
        product_instances = obj.get_products()
        return product_instances
    class Meta:
        model = Basket
        fields = ['id', 'title', 'products']


class FavoriteSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    def get_products(self, obj):
        product_instances = obj.get_products()
        return product_instances
    class Meta:
        model = Favorite
        fields = ['id', 'title', 'products']