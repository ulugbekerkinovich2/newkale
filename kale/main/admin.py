from django.contrib import admin

from kale.main.models import Product, ProductShots, ProductCategory, ProductUpdateLog


class ProductShotsInline(admin.TabularInline):
    model = ProductShots
    extra = 0


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductShotsInline]
    list_display = ["title_ru", "unit", "category"]
    raw_id_fields = ["category"]
    # list_select_related = ["category"]
    # list_filter = ["category"]

@admin.register(ProductShots)
class ProductShotsAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductUpdateLog)
class ProductUpdateLogAdmin(admin.ModelAdmin):
    pass
