from abc import ABC, abstractmethod
from ..client.tap_openmeteo_client import TapOpenMeteoClient

#Abstração criada para garantir que o client será chamado corretamente

class BaseOpenMeteoExtractor(ABC):
    def __init__(self, endpoint, config):
        """
        endpoint: qual endpoint será usado ('v1/forecast' etc)
        config: config dict que já deve conter os params
        """
        self.config = config
        params = config.get("params", {})
        self.client = TapOpenMeteoClient(endpoint, params)

    @abstractmethod
    def extract(self):
        pass
