import urllib.parse
from datetime import date, datetime

import urllib3
from requests import get

from src.domain.ean import GoogleSearchEAN
from src.domain.product_page import GoogleProductPage
from src.domain.stores import GoogleStores
from src.features.get_systems import available_systems
from src.features.handlers.base_handler import AbstractHandler
from src.helpers.queue_consumers_and_producers import ProductsQueue
from src.repositories.comparison import ComparisonRepository
from src.repositories.stores import StoresRepository
from src.utils.enumerators import EanSearchStatus
from src.utils.headers import build_general_header
from src.utils.strings import normalize_text
from src.utils.vtex_site_validator import extract_subdomain_if_is_vtex

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


STATUS_TO_FROM = {
    EanSearchStatus.UNIQUE_STORE.value: EanSearchStatus.SUCCESS.value,
    EanSearchStatus.MULTIPLE_RESULTS.value: EanSearchStatus.MULTIPLE_RESULTS.value,
}


class SearchEan(AbstractHandler):
    def __init__(self, session=None, headers=None):
        self.session = session
        self.headers = headers

    def handle(self, request):

        if isinstance(request, str):
            # request is the EAN
            ean = request
        elif isinstance(request, dict) and request.get("ean"):
            ean = request.get("ean")
        else:
            raise ValueError(
                "EAN must be passed as string or a dict like {'ean': '1234567890'}"
            )

        result = GoogleSearchEAN(ean, session=self.session, headers=self.headers).run()

        status = result.get("status")
        if status in (
            EanSearchStatus.UNIQUE_STORE.value,
            EanSearchStatus.MULTIPLE_RESULTS.value,
        ):
            return {
                "crawled": True,
                "status": STATUS_TO_FROM[status],
                "product_link": result["product_link"],
                "step": "SearchEan",
            }
        elif status == EanSearchStatus.SUCCESS.value:
            return super().handle(result)
        return {"crawled": False, "step": "SearchEan"}


class ProductPage(AbstractHandler):
    def __init__(self, session=None, headers=None):
        self.session = session
        self.headers = headers

    def handle(self, request: dict):
        if product_link := request.get("product_link"):
            result = GoogleProductPage(
                product_link, session=self.session, headers=self.headers
            ).run()

            result.update(request)

            if result["ean"].lstrip("0") != result["search_ean"].lstrip("0"):
                print(
                    f"The ean searched {result['search_ean']} is not equal "
                    f"to the ean found {result['ean']}. Stopping!"
                )
                return {
                    "crawled": True,
                    "status": EanSearchStatus.NOT_FOUND.value,
                    "step": "ProductPage",
                }
            elif result.get("all_stores_links"):
                return super().handle(result)
            return {
                "crawled": False,
                "status": EanSearchStatus.NOT_FOUND.value,
                "step": "ProductPage",
            }

        raise ValueError("'product_link' must to be a key from dict.")


class Stores(AbstractHandler):
    def __init__(self, session=None, headers=None):
        self.session = session
        self.headers = headers

    def handle(self, request):
        if all_stores_links := request.get("all_stores_links"):
            google_stores = GoogleStores(
                all_stores_links, session=self.session, headers=self.headers
            )
            google_stores.run()

            result = {"google_stores": google_stores}
            result.update(request)

            if len(google_stores.stores) > 0:
                return super().handle(result)
            return {"crawled": False, "status": EanSearchStatus.NOT_FOUND.value}

        raise ValueError("'all_stores_links' must to be a key from dict.")


class SaveStores(AbstractHandler):
    _available_systems_in_postgres: dict = {}

    def handle(self, request: dict):
        """
            It receives from last handler a dict with all info collect until now,
        and one of those is "google_stores", who is very important to us
        process all products and your market place.

            The dict will be something link:

        {
            'all_stores_links': 'The url to redirect to all stores in google',
            'brand': 'The brand of the product',
            'description': 'A description for the product',
            'ean': 'The ean of the product',
            'google_stores': <instance> GoogleStores, # The most important field who
                                                      # contains information what we
                                                      # need
            'img': 'The url for the google img from this product',
            'name': 'The name of the product on the google',
            'product_link': 'The link for the product in google search',
            'search_ean': 'The ean used to search on google query',
            'skus': [
                '0140230319',
                '024004002',
                '04697',
                '10021133',
            ],
            'status': 's'
        }

            The field instance of the class GoogleStores, has an attribute named as
        stores, who contains a list of a named tuple that has the fields:
           # "name": store_ref
           # "product_price": product price on google
           # "redirect_link": the link of the market place

        GoogleStores.stores -> Structure bellow

            List[
                namedtuple(
                    "Stores",
                    "name product_price redirect_link"
                )
           ]

        @param request: Dict
        @return: bool or redirect to the super().handle()
        """
        if request and "google_stores" in request:
            self._available_systems_in_postgres = available_systems()

            all_stores_class: GoogleStores = request["google_stores"]
            all_stores_list = all_stores_class.stores
            products_list = [
                {
                    "product_name_on_google": request["name"],
                    "brand": request["brand"],
                    "ean": request["ean"],
                    "price_on_google": store.product_price,
                    "store_name": self._get_store_name(store.name),
                    "store_ref": store.name.upper().strip(),
                    "product_link": store.redirect_link,
                    "ads": store.more_ads,
                    "img": request["img"],
                    "system": self._handle_crawler_system(
                        store.name.upper().strip(), store.redirect_link,
                    )
                    or store.name,
                    "store_id": (
                        self._available_systems_in_postgres.get(
                            store.name.upper().strip(), {}
                        ).get("store_id", 0)
                    ),
                    "metadata": {
                        "inserted_at": datetime.now(),
                        "updated_at": None,
                        "crawled": False,
                    },
                }
                for store in all_stores_list
            ]

            ProductsQueue.insert_products_on_queue(products_list)
            today_reference = str(date.today())
            hour_reference = datetime.now().strftime("%H:%M:%S.%f")

            ComparisonRepository.save(
                [
                    {
                        "ean": product["ean"],
                        "store_id": product["store_id"],
                        "price_to": product["price_on_google"],
                        "date": today_reference,
                        "hour": hour_reference,
                    }
                    for product in products_list
                ]
            )
            request["crawled"] = True
            request["status"] = EanSearchStatus.SUCCESS.value
            request["step"] = "SaveStores"
            return super().handle(request)

        # Something went wrong and isn't possible to found
        # the product from this ean
        return {
            "crawled": False,
            "status": EanSearchStatus.NOT_FOUND.value,
            "step": "SaveStores",
        }

    def _handle_crawler_system(self, store_ref: str, store_url: str):
        store_ref = store_ref.replace("'", "")

        if store_item := self._available_systems_in_postgres.get(store_ref.upper()):
            return store_item.get("platform", "SYSTEM")

        # The store doesn't exist on database
        # Let's save it on the table
        if platform_url := self._discovery_platform_url(store_url):
            new_store = {
                "store_name": normalize_text(store_ref),
                "store_ref": store_ref,
                "store_table": self._build_table_name(store_ref),
                "seller_default": normalize_text(store_ref),
                "url": platform_url,
            }

            if vtex_sub_domain := extract_subdomain_if_is_vtex(store_url):
                new_store["platform"] = "VTEX"
                new_store["subdomain_platform"] = vtex_sub_domain

            # Saving the new store
            StoresRepository.save(new_store)
            print(new_store)
        return store_ref

    def _get_store_name(self, store_ref: str):
        if store_item := self._available_systems_in_postgres.get(store_ref):
            return store_item.get("store_name", store_ref)
        return store_ref

    @staticmethod
    def _build_table_name(store_ref: str):
        store_ref = normalize_text(store_ref)
        store_ref = (
            store_ref.lower()
            .replace(".com.br", "")
            .replace(".com", "")
            .replace("&", "e")
        )
        for char in [".", "!", "?", ":", "@", "#", "$", "%", "-"]:
            store_ref = store_ref.replace(char, " ")
        return "_".join(store_ref.strip().split())

    @staticmethod
    def _discovery_platform_url(redirect_url):
        try:
            response = get(redirect_url, headers=build_general_header(), verify=False)
            url_parsed = urllib.parse.urlsplit(response.request.url)
            return f"{url_parsed.scheme}://{url_parsed.netloc}"
        except Exception:
            return None
