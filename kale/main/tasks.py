from datetime import datetime

import pytz
from django.core.exceptions import MultipleObjectsReturned

from config import celery_app
from kale.main.models import ProductCategory, Product, ProductUpdateLog, ProductUnitChoices
from kale.utils.one_s_get_products import get_products, get_latest_update_datetime


@celery_app.task()
def update_products():
    """A pointless Celery task to demonstrate usage."""
    # 1 step checking update times
    last_update_from_one_s = get_latest_update_datetime()["Дата последнего изменения остатков"]
    last_update_from_one_s_obj = datetime.strptime(last_update_from_one_s, "%d.%m.%Y %H:%M:%S")
    update_log_obj = ProductUpdateLog.objects.all().first()
    tashkent_tz = pytz.timezone("Asia/Tashkent")
    if (
        update_log_obj and
        last_update_from_one_s_obj == update_log_obj.updated_date.astimezone(tashkent_tz).replace(tzinfo=None)
    ):
        return False
    # 2 step. If updated from 1c change DB
    products = get_products()
    category_dict = dict()
    product_objects = []
    for json_obj in products["Товары"]:
        # CREATING CATEGORY OBJECT
        name_of_category = json_obj["Категория"]
        category_obj = category_dict.get(name_of_category)
        if category_obj is None:
            # Поиск в локальном словаре category_dict
            if name_of_category == "":
                # Если есть пустые назовем
                name_of_category = "Без названия"
            category_qs = ProductCategory.objects.filter(name_ru=name_of_category)
            if category_qs.exists():
                category_dict.update(
                    {name_of_category: category_qs.first()}
                )

        # Поиск продуктов
        name_of_product = json_obj["Наименование"]
        if name_of_product == "":
            name_of_product = "Без названия"
        try:
            Product.objects.get(title_ru=name_of_product, category=category_obj)
        except Product.DoesNotExist:
            product = Product.objects.create(title_ru=name_of_product,
                                             description_ru=json_obj['Описание'],
                                             price=json_obj['Цена'],
                                             category=category_obj,
                                             code=json_obj['Код'],
                                             rest_count=json_obj['Остаток'],
                                             unit=json_obj["ЕдиницаИзмерения"],
                                             is_float=True if ProductUnitChoices.M2 == json_obj[
                                                 "ЕдиницаИзмерения"] else False,
                                             manufacturer=json_obj['Производитель'],
                                             proportions=json_obj["Размеры"],
                                             brand=json_obj["ТорговаяМарка"], )
            product_objects.append(product)
        except MultipleObjectsReturned:
            pass
    update_datetime = get_products()["Дата последнего изменения остатков"]
    Product.objects.bulk_create(product_objects)
    update_datetime_obj = datetime.strptime(update_datetime, "%d.%m.%Y %H:%M:%S")
    ProductUpdateLog.objects.create(updated_date=update_datetime_obj)
    return True
