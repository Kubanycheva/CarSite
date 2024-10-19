from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name',
                  'last_name', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']


class ProductPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhotos
        fields = ['image']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    class Meta:
        model = Review
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    year = serializers.DateTimeField(format='%Y')
    price_dollar = serializers.SerializerMethodField()


    class Meta:
        model = Product
        fields = ['id', 'product_name', 'price', 'year', 'price_dollar']

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_price_dollar(self, obj):
        exchange_rate = 88.5
        return round(obj.price / exchange_rate, 2)



class ProductDetailSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    category = CategorySerializer()
    product = ProductPhotosSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    date = serializers.DateTimeField(format='%d-%m-%Y')
    owner = UserProfileSimpleSerializer()
    ratings = RatingSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'description', 'product', 'price', 'active', 'product_photos',
                  'average_rating', 'ratings', 'reviews', 'owner', 'date']

    def get_average_rating(self, obj):
        return obj.get_average_rating()