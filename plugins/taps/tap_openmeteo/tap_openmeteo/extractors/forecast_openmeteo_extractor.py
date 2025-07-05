from .base_openmeteo_extractor import BaseOpenMeteoExtractor

#Classe que implementa a abstração do base_openmeteo_extractor para o endpoint forecast

class ForecastOpenMeteoExtractor(BaseOpenMeteoExtractor):
    def __init__(self, config):
        super().__init__("v1/forecast", config)

    def extract(self):
        return self.client.get()
