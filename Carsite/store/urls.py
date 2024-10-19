from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('', ProductListViewSet.as_view({'get': 'list', 'post': 'create', }), name='product_list'),
    path('<int:pk>/', ProductDetailViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}), name='product_detail'),


    path('category', CategoryViewSet.as_view({'get': 'list', 'post': 'create', }), name='category_list'),
    path('category/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}), name='category_detail'),


    path('photo', ProductPhotosViewSet.as_view({'get': 'list', 'post': 'create', }), name='photo_list'),
    path('photo/<int:pk>/', ProductPhotosViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}), name='photo_detail'),


    path('review', ReviewViewSet.as_view({'get': 'list', 'post': 'create', }), name='review_list'),
    path('review/<int:pk>/', ReviewViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}), name='review_detail'),








]