from common.base_client import BaseClient

#Classe que implementa a abstração do base_openmeteo_extractor para o endpoint archive

class ArchiveOpenMeteoExtractor(BaseClient):
    def __init__(self, config):
        super().__init__("https://archive-api.open-meteo.com","v1/archive", config)

    def extract(self):
        return self.client.get()