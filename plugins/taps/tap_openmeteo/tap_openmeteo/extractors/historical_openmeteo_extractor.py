from common.base_client import BaseClient

#Classe que implementa a abstração do base_openmeteo_extractor para o endpoint historical

class HistoricalOpenMeteoExtractor(BaseClient):
    def __init__(self, config):
        super().__init__("https://api.open-meteo.com","v1/historical", config)

    def extract(self):
        return self.client.get()
