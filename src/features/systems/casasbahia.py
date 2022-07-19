from src.features.systems.viavarejobase import ViaVarejo


class CasasBahia(ViaVarejo):
    system = "casasbahia"
    base_url = "https://www.casasbahia.com.br/"

    def __init__(self, product_url):
        super().__init__(product_url, system_name="casasbahia")
