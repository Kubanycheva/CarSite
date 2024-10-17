from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(region='KG', null=True, blank=True)


class Category(models.Model):
    category_name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=32)
    description = models.TextField()
    year = models.DateTimeField()
    price = models.PositiveSmallIntegerField(default=0)
    active = models.BooleanField(verbose_name='в наличии', default=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    car_mileage = models.CharField(max_length=32, null=True, blank=True)
    car_body = models.CharField(max_length=32, null=True, blank=True)
    color = models.CharField(max_length=32)
    car_engine = models.CharField(max_length=32, null=True, blank=True)
    BOX_CHOICES = (
        ('автомат', 'АВТОМАТ'),
        ('механика', 'МЕХАНИКА')
    )
    box = models.CharField(max_length=10, choices=BOX_CHOICES, default='simple')
    DRIVE_CHOICES = (
        ('передний', 'ПЕРЕДНИЙ'),
        ('задний', 'ЗАДНИЙ'),
    )
    drive = models.CharField(max_length=10, choices=DRIVE_CHOICES, default='simple')
    RUL_CHOICES = (
        ('слева', 'СЛЕВА'),
        ('справа', 'СПРАВА')
    )
    rul = models.CharField(max_length=32, choices=RUL_CHOICES, default='simple')
    state = models.CharField(max_length=32, null=True, blank=True)
    tamozhnya = models.CharField(max_length=32, null=True, blank=True)
    region = models.CharField(max_length=32, null=True, blank=True)
    uchot = models.CharField(max_length=32, null=True, blank=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.product_name

    def get_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(rating.stars for rating in ratings) / ratings.count(), 1)
        return 0


class ProductPhotos(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/')


class Rating(models.Model):
    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(1, str(i)) for i in range(1, 6)], verbose_name='Рейтинг')

    def __str__(self):
        return f'{self.user}'


class Review(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    parent_review = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.product}'

