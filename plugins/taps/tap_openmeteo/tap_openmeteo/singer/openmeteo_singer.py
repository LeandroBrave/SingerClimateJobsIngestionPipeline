import json
from common.singer_emitter import SingerEmitter
import logging

class OpenMeteoSingerRunner:
    def __init__(self, extractor, catalog, stream_name):
        self.emitter = SingerEmitter()
        self.catalog = catalog
        self.extractor = extractor
        self.stream_name = stream_name

    def run(self):
        # 1. Extrai payload
        data = self.extractor.extract()

        # 2. Extrai todas as listas do bloco "hourly"
        hourly_data = data["hourly"]
        times = hourly_data["time"]
        variables = [k for k in hourly_data.keys() if k != "time"]

        # 3. Extrai schema e key_properties do catalog
        stream_info = next(s for s in self.catalog["streams"] if s["stream"] == self.stream_name)
        schema = stream_info["schema"]
        key_properties = stream_info.get("key_properties", [])

        # 4. Extrai apenas os metadados definidos no schema
        catalog_fields = schema["properties"].keys()
        metadata_fields = [f for f in catalog_fields if f not in variables and f != "time"]
        metadata = {f: data[f] for f in metadata_fields if f in data}

        # 5. Constrói lista de records
        records = []
        for idx, time in enumerate(times):
            record = {
                "time": time,
                **metadata
            }
            for var in variables:
                value = hourly_data.get(var, [None])[idx]
                record[var] = value
            records.append(record)

        # 6. Emite schema e records
        self.emitter.write_schema(self.stream_name, schema, key_properties)
        self.emitter.write_batch_records(self.stream_name, records)
