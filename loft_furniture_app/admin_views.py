from rest_framework import viewsets
from rest_framework.response import Response

from .models import *
from .admin_serializers import *


class CategoryViewSets(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class CategoryDetailView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        return Response(data)


class SubCategoryViewSets(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializers


class SubCategoryDetailView(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializers

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        return Response(data)


class BrandViewSets(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializers


class BrandDetailView(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializers

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        return Response(data)


class ColorViewSets(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorsSerializers


class ColorDetailView(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorsSerializers

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        return Response(data)


class CharacteristicViewSets(viewsets.ModelViewSet):
    queryset = Characteristic.objects.all()
    serializer_class = CharacterSerializers


class CharacteristicDetailView(viewsets.ModelViewSet):
    queryset = Characteristic.objects.all()
    serializer_class = CharacterSerializers

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        return Response(data)


class ImageViewSets(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializers


class ImageDetailView(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializers

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        return Response(data)


class AdminProductViewSets(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers


class AdminProductDetailView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        return Response(data)

