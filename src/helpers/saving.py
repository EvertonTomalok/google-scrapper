import logging
from collections import namedtuple

from src.repositories.dataquality import DataQualityRepository
from src.repositories.product import ProductRepository
from src.utils.enumerators import EanSearchStatus

logger = logging.getLogger(__name__)

StoreInfo = namedtuple("StoreInfo", "store_id store_table")

STORE = {
    "casasbahia": StoreInfo(96, "cnova"),
    "extra": StoreInfo(93, "cnova"),
    "pontofrio": StoreInfo(94, "cnova"),
    "magazineluiza": StoreInfo(89, "magazineluiza"),
}


def saving_product(product):
    if not product.get("provider"):
        return

    data = {
        "ean": product["ean"],
        "sku": product["sku"],
        "url": product["url"],
        "product_reference": product["model"],  # TODO CHECK this info
        "status": EanSearchStatus.SUCCESS.value,
        "seller_name": product["seller_name"],
    }

    if voltage := product["voltage"]:
        data["attribute_name"] = "VOLTAGEM"
        data["attribute_value"] = voltage
    elif color := product["color"]:
        data["attribute_name"] = "COR"
        data["attribute_value"] = color

    store_info = STORE.get(product["system"])
    data["store_id"] = store_info.store_id or 0
    try:
        ProductRepository.save(store_info.store_table, data)
    except Exception as err:
        logger.error(f"Couldn't product: {type(err)} -> {err}")


def saving_on_data_quality(product):
    allowed_fields = (
        "ean",
        "product_name",
        "brand",
        "image",
        "model",
        "provider",
        "color",
        "voltage",
    )
    try:
        filtered_product = {field: product[field] for field in allowed_fields}
        if image_on_google := product.get("img"):
            filtered_product["image_google"] = image_on_google
        DataQualityRepository.save(filtered_product)
    except Exception as err:
        logger.error(f"Couldn't saving_on_data_quality: {type(err)} -> {err}")
