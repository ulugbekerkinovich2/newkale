from django.contrib import admin

from kale.main.models import Product, ProductShots, ProductCategory, ProductUpdateLog


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductShots)
class ProductShotsAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductUpdateLog)
class ProductUpdateLogAdmin(admin.ModelAdmin):
    pass
