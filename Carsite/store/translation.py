from modeltranslation.translator import TranslationOptions, register
from .models import Product


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ['product_name', 'description']