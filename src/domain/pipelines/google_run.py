from src.features.handlers.google_handlers import (
    ProductPage,
    SaveStores,
    SearchEan,
    Stores,
)


def build_google_default_pipeline(session=None, headers=None):
    search_ean = SearchEan(session, headers)
    product_page = ProductPage(session, headers)
    stores = Stores(session, headers)
    save_stores = SaveStores()

    search_ean.set_next(product_page).set_next(stores).set_next(save_stores)

    return search_ean
