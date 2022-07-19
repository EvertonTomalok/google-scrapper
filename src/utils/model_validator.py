from logging import getLogger
from typing import Dict, Type, Union

from schematics import Model
from schematics.exceptions import DataError

logger = getLogger()


def validate_and_parse_model(data, cls: Type[Model]) -> Union[Dict, None]:
    try:
        model = cls(data)
        model.validate()
        return model.to_primitive()
    except DataError:
        return None
