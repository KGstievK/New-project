from django_filters.rest_framework import DjangoFilterBackend, BaseInFilter, RangeFilter
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from datetime import date
from rest_framework import permissions
from .serializers import *
from .my_permissions import *
from rest_framework.response import Response
from rest_framework_simplejwt import views
from rest_framework.exceptions import AuthenticationFailed, NotFound
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from rest_framework import status
import django_filters
from django.shortcuts import HttpResponse


class UserViewSets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        # Хешируем пароль перед сохранением пользователя
        password = make_password(self.request.data['password'])
        user_email = self.request.data['email']
        user_username = user_email.split('@')[0]
        serializer.save(password=password, username=user_username)

        # Получаем созданного пользователя
        user = serializer.instance

        # Создаем новую корзину для пользователя
        new_user_basket = Basket()
        new_user_basket.title = f"Корзина пользователя {user.firstName}"
        new_user_basket.save()
        user.basket = new_user_basket

        # Создаем новый объект Избранных продуктов для пользователя
        new_user_favorite = Favorite()
        new_user_favorite.title = f"Избранные продукты пользователя {user.firstName}"
        new_user_favorite.save()
        user.favorite = new_user_favorite

        # Сохраняем изменения в объекте пользователя
        user.save()


class UserDetailView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # def get_permissions(self):
    #     if self.action == 'retrieve':  # Для метода retrieve разрешаем доступ без авторизации
    #         permission_classes = [permissions.AllowAny]
    #     else:  # Для остальных методов сохраняем текущие разрешения
    #         permission_classes = [permissions.IsAuthenticatedOrReadOnly, CanEditOrDeleteUserExceptSuperuser]
    #     return [permission() for permission in permission_classes]
    # # permission_classes = [permissions.IsAuthenticatedOrReadOnly, CanEditOrDeleteUserExceptSuperuser]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        return Response(data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(f'instance: {instance}')
        data = request.data.copy()  # Создаем копию request.data, чтобы ее можно было изменить
        print(f'data: {data}')
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        if 'password' in data:
            instance.set_password(data['password'])

        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Удаляем связанные объекты Basket и Favorite, если они существуют
        if hasattr(instance, 'basket'):
            instance.basket.delete()
        if hasattr(instance, 'favorite'):
            instance.favorite.delete()

        # Затем удаляем самого пользователя
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegistrationView(views.TokenObtainPairView):

    def post(self, request):
        try:
            email = request.data['email']
            username = email.split('@')[0]
            first_name = request.data['firstName']
            last_name = request.data['lastName']
            password = request.data['password']

            user = User(
                email=email,
                firstName=first_name,
                lastName=last_name,
                username=username,
                password=password,
            )

            user.set_password(password)

            new_user_basket = Basket()
            new_user_basket.title = f"Корзина пользователя {user.firstName}"
            new_user_basket.save()
            user.basket = new_user_basket

            new_user_favorite = Favorite()
            new_user_favorite.title = f"Избранные продукты пользователя {user.firstName}"
            new_user_favorite.save()
            user.favorite = new_user_favorite

            user.save()

            user2 = User.objects.filter(email=user.email).first()

            if user2 is None:
                raise AuthenticationFailed('User not found!')

            if not user2.check_password(password):
                raise AuthenticationFailed('Incorrect password!')

            access_token = AccessToken.for_user(user2)

            return Response({
                'id': user2.pk,
                'firstName': user2.firstName,
                'lastName': user2.lastName,
                'email': user2.email,
                'jwt': str(access_token)
            })
        except KeyError:
            return Response({'error': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class LoginView(views.TokenObtainPairView):

    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']

            user = User.objects.filter(email=email).first()

            if user is None:
                raise AuthenticationFailed('User not found!')

            if not user.check_password(password):
                raise AuthenticationFailed('Incorrect password!')

            access_token = AccessToken.for_user(user)

            return Response({
                'id': user.id,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'email': user.email,
                'jwt': str(access_token),
            })
        except KeyError:
            return Response({'error': 'Missing required error'}, status=status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            data = serializer.data

            return Response(data)
        except NotFound:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProductFilter(django_filters.FilterSet):
    price = RangeFilter(field_name='price')  # Фильтр диапазона для цены

    class Meta:
        model = Product
        fields = ['category', 'brand', 'sub_category']


class ProductListView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', 'price', 'brand', 'sub_category', ]
    search_fields = ['name']

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BrandListView(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandDetailView(RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        return Response(data)


class AddReviewToProduct(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        try:
            user = request.user
            product = Product.objects.get(id=id)

            new_review = Review()
            new_review.title = request.data['title']
            new_review.date = date.today()
            new_review.user = user
            new_review.product = product
            new_review.save()

            rev_ser = ReviewSerializer(new_review).data

            return Response(rev_ser)
        except Product.DoesNotExist:
            raise Http404("Product does not exist!")
        except KeyError:
            return Response({'error': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AddProductToBasket(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        try:
            user = request.user
            # product = Product.objects.get(id=id)
            product = get_object_or_404(Product, pk=id)

            if user.basket is None:
                new_user_basket = Basket()
                new_user_basket.title = f"Корзина пользователя {user.firstName}"
                new_user_basket.save()
                user.basket = new_user_basket
                user.save()

            product.baskets.add(user.basket)
            product.save()

            return JsonResponse({'success': 'Product added to basket'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class AddProductToFavorite(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        try:
            user = request.user
            # product = Product.objects.get(id=id)
            product = get_object_or_404(Product, pk=id)

            if user.favorite is None:
                new_user_favorite = Favorite()
                new_user_favorite.title = f"Избранные продукты пользователя {user.firstName}"
                new_user_favorite.save()
                user.favorite = new_user_favorite
                user.save()

            product.favorites.add(user.favorite)
            product.save()

            return JsonResponse({'success': 'Product added to favorite'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class ChangeRatingToProduct(APIView):
    def patch(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        new_rating = request.data.get('rating')

        if new_rating is not None:
            try:
                new_rating = float(new_rating)
                if not 0 <= new_rating <= 5:
                    return JsonResponse({'error': 'Rating should be between 0 and 5'}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return JsonResponse({'error': f'Invalid rating format. Instead: ({new_rating}) write number!'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                product.rating = new_rating
                product.save(update_fields=['rating'])
                return JsonResponse({'success': 'Rating added to product'})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse({'error': 'No rating provided'}, status=status.HTTP_400_BAD_REQUEST)


class ChangeRatingToReview(APIView):
    def patch(self, request, id):
        try:
            review = Review.objects.get(id=id)
        except Review.DoesNotExist:
            return JsonResponse({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

        new_rating = request.data.get('rating')

        if new_rating is not None:
            try:
                new_rating = float(new_rating)
                if not 0 <= new_rating <= 5:
                    return JsonResponse({'error': 'Rating should be between 0 and 5'},
                                        status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return JsonResponse({'error': f'Invalid rating format. Instead: ({new_rating}) write number!'},
                                    status=status.HTTP_400_BAD_REQUEST)

            try:
                review.rating = new_rating
                review.save(update_fields=['rating'])
                return JsonResponse({'success': 'Rating added to review'})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse({'error': 'No rating provided'}, status=status.HTTP_400_BAD_REQUEST)


class GetBasketProducts(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            user = request.user
            basket = user.basket
            # basket_products = Product.objects.filter(basket_id=basket.pk)
            products = basket.basket_products.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Basket.DoesNotExist:
            raise NotFound("Basket not found for the current user.")
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetFavoriteProducts(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            user = request.user
            favorite = user.favorite
            # fav_products = Product.objects.filter(favorite_id=user.favorite.pk)
            products = favorite.favorite_products.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Favorite.DoesNotExist:
            raise NotFound("Favorite not found for the current user!")
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetAllNewProducts(APIView):
    def get(self, request):
        new_products = Product.objects.filter(new=True)
        serializer = ProductSerializer(new_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDiscountListView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.exclude(discount=None)


class RemoveProductFromBasket(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, id):
        # Получаем данные из запроса
        user = request.user
        product = Product.objects.get(id=id)

        # Проверяем, существуют ли пользователь и продукт
        try:
            user = request.user
            product = Product.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Product.DoesNotExist:
            return Response({"message": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Получаем корзину пользователя
        basket = Basket.objects.get(id=user.basket.pk)

        # Удаляем продукт из корзины, если он там есть
        if product in basket.basket_products.all():
            basket.basket_products.remove(product)
            return Response({"message": "Product removed from basket"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Product not found in user's basket"}, status=status.HTTP_404_NOT_FOUND)


class RemoveAllProductsFromBasket(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            basket = Basket.objects.get(user=user)
            basket.basket_products.clear()
            return Response({"message": "All products removed from basket"}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": "Basket not found for the current user"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReviewListView(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
