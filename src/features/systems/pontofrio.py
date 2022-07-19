from src.features.systems.viavarejobase import ViaVarejo


class PontoFrio(ViaVarejo):
    system = "pontofrio"
    base_url = "https://www.pontofrio.com.br/"

    def __init__(self, product_url):
        super().__init__(product_url, system_name="pontofrio")
