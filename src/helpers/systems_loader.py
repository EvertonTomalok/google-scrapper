import importlib
import inspect
import os
from typing import Dict, List, Type

from src.features.systems.base import SystemTemplate


def _filter_modules(modules_list: List[str]) -> Dict[str, str]:
    """
        Filter the modules from the path, to get only .py ending and not
    containing double underscores.

    @param modules_list: List[str]
    @return: Dict[module_name, module_path]
    """

    module_dict = {}

    for module in modules_list:
        if module.endswith(".py") and "base" not in module and "__" not in module:
            module_name = module.replace(".py", "")
            module_dict[module_name] = f"src.features.systems.{module_name}"

    return module_dict


def _list_modules() -> Dict[str, str]:
    """
        It will list modules from src/helpers/systems, filtering by modules python that
    ends with .py and not is double underscore.

    @return: List[str]
    """
    return _filter_modules(os.listdir("src/features/systems"))


def load_system_classes(system: str) -> List[Type[SystemTemplate]]:
    """
        Load the module and get the class from the system...
    Like 'magazineluiza' will return the module 'src/helpers/systems/magazineluiza.py'
    with your systems classes in a list like:

        - [<class 'src.features.systems.magazineluiza.MagazineLuiza'>].


    @param system: STR -> the name from the system, like 'magazineluiza' or 'casasbahia'
    @return: List[Type[SystemTemplate]]
    """
    modules = _list_modules()

    if module_path := modules.get(system.lower()):
        module = importlib.import_module(module_path)
        return [
            cls
            for _, cls in inspect.getmembers(module)
            if inspect.isclass(cls)
            and issubclass(cls, SystemTemplate)
            and cls is not SystemTemplate
            and system.lower() == cls.system
        ]
    return []
