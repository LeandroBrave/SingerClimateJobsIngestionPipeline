from common.base_client import BaseClient

#Classe que implementa a abstração do base_openmeteo_extractor para o endpoint forecast

class ForecastOpenMeteoExtractor(BaseClient):
    def __init__(self, config):
        super().__init__("https://api.open-meteo.com","v1/forecast", config)

    def extract(self):
        return self.client.get()
