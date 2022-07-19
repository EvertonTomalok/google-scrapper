from schematics.models import Model, ValidationError
from schematics.types import IntType, StringType, URLType


def is_status_allowed(status_type):
    if status_type.upper() in ("S", "N"):
        return status_type.upper()
    raise ValidationError("The value from status must to be 'S' or 'N'.")


class StoreModel(Model):
    store_name = StringType(required=True)
    store_ref = StringType(required=True)
    store_id = IntType(default=0)
    status = StringType(default="N", validators=[is_status_allowed])
    platform = StringType(required=False)
    store_table = StringType(required=True)
    seller_default = StringType(required=True)
    subdomain_platform = StringType(required=False)
    url = URLType(required=True)

    class Options:
        serialize_when_none = False
