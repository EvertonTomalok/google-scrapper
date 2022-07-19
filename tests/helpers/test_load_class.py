from src.features.systems.magazineluiza import MagazineLuiza
from src.helpers.systems_loader import load_system_classes


def test_load_system():
    list_cls = load_system_classes('magazineluiza')
    cls = list_cls[0]

    assert issubclass(cls, MagazineLuiza)


def test_load_system_not_exists():
    list_cls = load_system_classes('modulonaoexiste')

    assert not list_cls
