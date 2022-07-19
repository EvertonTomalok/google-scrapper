from src.features.handlers.store_spiders_handlers import (
    LoadSystem,
    RunSystem,
    SaveProduct,
)


def build_spider_pipeline():
    load_system = LoadSystem()
    run_system = RunSystem()
    save_product = SaveProduct()

    load_system.set_next(run_system).set_next(save_product)

    return load_system
