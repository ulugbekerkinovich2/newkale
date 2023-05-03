from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductUnitChoices(models.TextChoices):
    M2 = ("м2", "м2")
    PIECE = ("шт", "шт")


class ProductCategory(models.Model):
    name_ru = models.CharField(_("Название категории ru"), max_length=100)
    name_uz = models.CharField(_("Kategoriya nomi uz"), max_length=100, null=True, blank=True)
    name_en = models.CharField(_("Product category en"), max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _("Бренд")
        verbose_name_plural = _("Бренды")

    def __str__(self):
        return self.name_uz


class Product(models.Model):
    title_ru = models.CharField(_("Наименование товара ru"), max_length=255, null=True, blank=True)
    title_uz = models.CharField(_("Tovar nomi uz"), max_length=255, null=True, blank=True)
    title_en = models.CharField(_("Product name en"), max_length=255, null=True, blank=True)
    code = models.CharField(_("Код товара"), max_length=50, null=True, blank=True)
    unit = models.CharField(_("Единица измерения"), choices=ProductUnitChoices.choices,
                            default=ProductUnitChoices.PIECE, max_length=10)
    brand = models.CharField(_("Торговая марка"), max_length=50, null=True, blank=True)
    proportions = models.CharField(_("Размеры"), max_length=30)
    description_ru = models.TextField(_("Описание ru"), null=True, blank=True)
    description_uz = models.TextField(_("Tavsif uz"), null=True, blank=True)
    description_en = models.TextField(_("Description en"), null=True, blank=True)
    manufacturer = models.CharField(_("Производитель"), max_length=20, null=True, blank=True)
    category = models.ForeignKey("main.ProductCategory", on_delete=models.PROTECT, null=True, blank=True)
    rest_count = models.FloatField(_("Остаток товара"), default=0)
    is_float = models.BooleanField(_("Остаток является нецелым"), default=False)
    price = models.IntegerField(_("Цена"), default=0)
    is_deleted = models.BooleanField(_("Удален ли товар"), default=False)

    class Meta:
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")

    def __str__(self):
        return self.title_ru if self.title_ru else _("Не заполнено")


class ProductShots(models.Model):
    product = models.ForeignKey("main.Product", on_delete=models.CASCADE)
    image = models.ImageField(_("Изображение"))

    class Meta:
        verbose_name = _("Изображение товара")
        verbose_name_plural = _("Изображения товаров")


class ProductUpdateLog(models.Model):
    updated_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ["-created_at"]
