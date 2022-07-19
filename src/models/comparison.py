from schematics.models import Model
from schematics.types import DateType, FloatType, IntType, StringType


class Comparison(Model):
    ean = IntType(required=True)
    store_id = IntType(required=True)
    price_to = FloatType(required=True)
    date = DateType(required=True)
    hour = StringType(required=True)
