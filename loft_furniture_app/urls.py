from django.urls import path, include
from .views import *
from .admin_views import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.generators import OpenAPISchemaGenerator

class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):

        swagger = super().get_schema(request, public)
        swagger.tags = [
            {
                "name": "registration",
                "description": "New user can register on the site"
            },
            {
                "name": "login",
                "description": "User can login using his email and password"
            },
            {
                "name": "product",
                "description": "Get product by product id"
            },
            {
                "name": "products",
                "description": "Get all products"
            },
            {
                "name": "addReview",
                "description": "An authorized user can add a review for the selected product"
            },
            {
                "name": "addProductToBasket",
                "description": "An authorized user can add a product to their basket"
            },
            {
                "name": "addProductToFavorite",
                "description": "An authorized user can add a product to their favorite"
            },
            {
                "name": "addRating",
                "description": "An authorized user can add a rating for the selected product"
            },
            {
                "name": "addRatingToReview",
                "description": "All users can add a rating to a review"
            },
            {
                "name": "getBasketProducts",
                "description": "Get all basket products for current user"
            },
            {
                "name": "getFavoriteProducts",
                "description": "Get all favorite products for current user"
            },
            {
                "name": "brand",
                "description": "get brand by id"
            },
            {
                "name": "brands",
                "description": "get all brands"
            },

        ]

        return swagger

schema_view = get_schema_view(
    openapi.Info(
        title="Swagger documentation",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
    generator_class=CustomOpenAPISchemaGenerator,
)

urlpatterns = [
    path('registration', RegistrationView.as_view(), name='registration'),
    path('login', LoginView.as_view(), name='login'),

    path('users', UserViewSets.as_view({'get': 'list', 'post': 'create'}), name='user_list'),
    path('user/<int:pk>', UserDetailView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='user_detail'),

    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products', ProductListView.as_view({'get': 'list'}), name='product-list'),

    path('addProductToBasket/<int:id>', AddProductToBasket.as_view(), name='add_product_to_basket'),
    path('addProductToFavorite/<int:id>', AddProductToFavorite.as_view(), name='add_product_to_favorite'),
    path('addReview/<int:id>', AddReviewToProduct.as_view(), name='add_review'),
    path('addRating/<int:id>', ChangeRatingToProduct.as_view(), name='add_rating'),
    path('addRatingToReview/<int:id>', ChangeRatingToReview.as_view(), name='add_rating_to_review'),

    path('getBasketProducts', GetBasketProducts.as_view(), name='get_bas_prod'),
    path('getFavoriteProducts', GetFavoriteProducts.as_view(), name='get_fav_prod'),
    path('getAllNewProducts', GetAllNewProducts.as_view(), name='get_new_products'),
    path('products_discount', ProductDiscountListView.as_view({'get': 'list'}), name='products_discount-list'),

    path('removeProductFromBasket/<int:id>', RemoveProductFromBasket.as_view(), name='remove_product_from_basket'),
    path('removeAllProductsFromBasket', RemoveAllProductsFromBasket.as_view(), name='remove_all_products_from_basket'),

    path('category/<int:pk>/', CategoryDetailView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='category-detail'),
    path('categories', CategoryViewSets.as_view({'get': 'list', 'post': 'create'}), name='category-list'),

    path('sub_category/<int:pk>/', SubCategoryDetailView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='category-detail'),
    path('sub_categories', SubCategoryViewSets.as_view({'get': 'list', 'post': 'create'}), name='category-list'),

    path('brand/<int:pk>/', BrandDetailView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='brand-detail'),
    path('brands', BrandListView.as_view({'get': 'list', 'post': 'create'}), name='brand-list'),

    path('color/<int:pk>/', ColorDetailView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='color-detail'),
    path('colors', ColorViewSets.as_view({'get': 'list', 'post': 'create'}), name='color-list'),

    path('characteristic/<int:pk>/', CharacteristicDetailView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='characteristic-detail'),
    path('characteristics', CharacteristicViewSets.as_view({'get': 'list', 'post': 'create'}), name='characteristic-list'),

    path('image/<int:pk>/', ImageDetailView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='image-detail'),
    path('images', ImageViewSets.as_view({'get': 'list', 'post': 'create'}), name='image-list'),

    path('admin_product/<int:pk>/', AdminProductDetailView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='admin_product-detail'),
    path('admin_products', AdminProductViewSets.as_view({'get': 'list', 'post': 'create'}), name='admin_product-list'),

    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('reviews', ReviewListView.as_view({'get': 'list'}), name='review-list'),

]
