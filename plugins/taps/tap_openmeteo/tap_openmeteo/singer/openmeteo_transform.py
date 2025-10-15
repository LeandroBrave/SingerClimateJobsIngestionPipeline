import logging
import os
import json

from singer import Transformer
from typing import List 

LOGGER = logging.getLogger('tap_openmeteo')

class OpenMeteoTransformer():
    def __init__(self, stream):
        self.stream = stream
        self._load_schema()
        LOGGER.debug(f"[OpenMeteoTransformer] {self.schema=}")


    def _load_schema(self):
        """
        Carrega o schema do catalog.json correspondente ao stream.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        catalog_path = os.path.abspath(os.path.join(current_dir, "..", "catalog", "catalog.json"))

        LOGGER.debug(f"[HCMTransformer] catalog_path={catalog_path}")

        if not os.path.exists(catalog_path):
            raise FileNotFoundError(f"catalog.json não encontrado: {catalog_path}")

        with open(catalog_path) as f:
            catalog = json.load(f)

        for s in catalog["streams"]:
            if s["stream"] == self.stream:
                self.schema = s["schema"]
                break
        else:
            raise ValueError(f"Stream {self.stream} não encontrado no catalog.json")


    def transform(self, data) -> List:
        records = []

        with Transformer() as transformer:
            for r in data['value']:
                try:
                    records.append(transformer.transform(r, self.schema))
                except Exception as ex:
                    LOGGER.debug(f"[OpenMeteoTransformer]  {r=}")
                    raise
        
        return records