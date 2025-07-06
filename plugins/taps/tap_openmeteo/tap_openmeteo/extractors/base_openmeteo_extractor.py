from abc import ABC, abstractmethod
from common.requests_client import RequestsClient

#Abstração criada para garantir que o client será chamado corretamente

class BaseOpenMeteoExtractor(ABC):
    def __init__(self, base_url, endpoint, config):
        """
        base_url: string, ex: https://api.open-meteo.com
        endpoint: qual endpoint será usado ('v1/forecast' etc)
        config: config dict que já deve conter os params
        """
        self.config = config
        params = config.get("params", {})
        self.client = RequestsClient(base_url, endpoint, params)

    @abstractmethod
    def extract(self):
        pass
