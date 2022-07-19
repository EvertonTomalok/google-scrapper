from schematics.models import Model
from schematics.types import IntType, StringType, URLType


class DataQuality(Model):
    ean = IntType(required=True)
    product_name = StringType(default="")
    brand = StringType()
    image = URLType(required=False, serialize_when_none=False)
    image_google = URLType(required=False, serialize_when_none=False)
    model = StringType()
    provider = StringType(default="")
    color = StringType()
    voltage = StringType()

    class Options:
        serialize_when_none = False
