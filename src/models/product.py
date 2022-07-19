from schematics.models import Model
from schematics.types import IntType, StringType, URLType


class Product(Model):
    ean = IntType(required=True)
    sku = StringType(required=True)
    product_reference = StringType()
    url = URLType(required=True)
    status = StringType(default="N")
    attribute_name = StringType()
    attribute_value = StringType()
    seller_name = StringType()
    store_id = IntType(required=True)
    url_raw = StringType()

    class Options:
        serialize_when_none = False
