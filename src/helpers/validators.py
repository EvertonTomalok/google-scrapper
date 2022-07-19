from collections import namedtuple

from schematics.exceptions import DataError

from src.utils.enumerators import Status

ModelStatus = namedtuple("ModelStatus", "status data")


def parse_model_and_validate(data: dict, cls) -> ModelStatus:
    """
    This function handles the data received. Before returning data,
    it checks if the data is in the correct model.
    :param data: Dict
    :param cls: Some class who inherit from schematics.models.Model

    :raises: schematics.exceptions.DataError

    :return: Dict
    """
    model = cls(data)
    try:
        model.validate()
        return ModelStatus(Status.success.value, model.to_primitive())
    except DataError as err:
        fields_errors = [{k: str(err.messages[k][0])} for k in err.messages.keys()]
        return ModelStatus(
            Status.error.value,
            {"fields_with_error": fields_errors, "data_received": data},
        )
