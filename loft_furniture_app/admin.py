from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin


User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ('email',)
    username = None
    list_display = ('email', 'firstName', 'lastName')
    list_filter = ["is_staff"]

    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        (
            "Other info",
            {
                "fields": [
                    "username",
                    "firstName",
                    "lastName",
                    "phone_number",
                    "image",
                    "is_active",
                    "is_staff",
                    "address",
                ],
            },
        ),
    ]
    add_fieldsets = [
        (
            None,
            {
                "fields": [
                    "email",
                    "firstName",
                    "lastName",
                    "password1",
                    "password2",

                    "is_active",
                    "is_staff",
                ]
            },
        ),
    ]


class ImageInline(admin.TabularInline):
    model = Image
    extra = 5
    max_num = 5


class CharacteristicInline(admin.TabularInline):
    model = Characteristic


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ("id", "name", "category", "sub_category", )
    list_display_links = ("name", )
    inlines = [ImageInline, ReviewInline]
    readonly_fields = ('get_html_photo', )
    list_filter = ("name", "category", "id")
    search_fields = ("name", )
    # fields = (('price', 'rating', 'in_stock', ), )
    fieldsets = (
        ('ADD NEW PRODUCT', {
            'fields': (('name', 'price', 'discount', 'rating', 'in_stock', 'new'), ),
        }),
        (None, {
            'fields': ('description', ),
        }),
        (None, {
            'fields': (('category', 'sub_category', 'brand'),),
        }),
        ('COLORS AND CHARACTERISTICS', {
            'fields': (('colors', 'characteristics'),),
        }),
    )

    def get_html_photo(self, object):
        images = object.get_image()
        if images:
            html = ""
            for image in images:
                html += f"<img src='http://127.0.0.1:8000/{image}' width=100 height=80>"
            return mark_safe(html)

    get_html_photo.short_description = "Images"


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_html_photo', 'image', )
    readonly_fields = ('image', 'get_html_photo',)

    def get_html_photo(self, object):
        img = object.image
        print(f'image: http://127.0.0.1:8000/{img.url}')
        if object.image:
            return mark_safe(f"<img src='http://127.0.0.1:8000/media/{img}' width=50>")


@admin.register(Characteristic)
class CharacteristicAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'value', )
    list_display_links = ('title', )
    list_filter = ("title", "id")
    search_fields = ("title", )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('title', )


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 0


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    # inlines = [ProductInline]
    list_display_links = ('title', )


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    inlines = [SubCategoryInline]
    list_display = ("id", "title", )
    list_display_links = ("title", )


admin.site.register(SubCategory)
admin.site.register(Color)
admin.site.register(Review)
admin.site.register(Address)
