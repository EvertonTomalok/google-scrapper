from src.features.systems.viavarejobase import ViaVarejo


class Extra(ViaVarejo):
    system = "extra"
    base_url = "https://www.extra.com.br/"

    def __init__(self, product_url):
        super().__init__(product_url, system_name="extra")
