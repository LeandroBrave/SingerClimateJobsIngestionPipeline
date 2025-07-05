import json
from common.singer_emitter import SingerEmitter

import logging

class OpenMeteoSingerRunner:
    def __init__(self, extractor, catalog_path, stream_name):
        """
        :param catalog_path: caminho do arquivo JSON com o catalog.
        """
        self.emitter = SingerEmitter()
        self.catalog = self._load_catalog(catalog_path)
        self.extractor = extractor
        self.stream_name = stream_name

    def _load_catalog(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def run(self):
        """
        Emite o SCHEMA e os RECORDS.
        :param stream_name: nome do stream (ex.: "forecast").
        :param records: lista de dicts extraídos.
        """
    
        # 1. Extrai payload
        data = self.extractor.extract()
        logging.info(data)
        # 2. Extrai as listas com os dados do clima
        times = data["hourly"]["time"]
        temps = data["hourly"]["temperature_2m"]

        # 3. Extrai os metadados 
        metadata = {
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "generationtime_ms": data["generationtime_ms"],
            "utc_offset_seconds": data["utc_offset_seconds"],
            "timezone": data["timezone"],
            "timezone_abbreviation": data["timezone_abbreviation"],
            "elevation": data["elevation"],
            "hourly_units": data["hourly_units"]
        }
        
        # 4. Constrói lista de records
        records = []
        for time, temp in zip(times, temps):
            record = {
                "time": time,
                "temperature_2m": temp,
                **metadata   # adiciona todos os metadados
            }
            records.append(record)
        
        # 5. Extrai schema e key_properties do catalog
        stream_info = next(s for s in self.catalog["streams"] if s["stream"] == self.stream_name)
        schema = stream_info["schema"]
        key_properties = stream_info.get("key_properties", [])

        # 6. Emite schema
        self.emitter.write_schema(self.stream_name, schema, key_properties)

        # 7. Emite todos os records
        self.emitter.write_batch_records(self.stream_name, records)