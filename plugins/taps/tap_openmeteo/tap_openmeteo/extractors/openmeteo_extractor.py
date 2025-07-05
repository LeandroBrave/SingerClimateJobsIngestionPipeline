from tap_openmeteo.extractors.forecast_openmeteo_extractor import ForecastOpenMeteoExtractor
from tap_openmeteo.extractors.historical_openmeteo_extractor import HistoricalOpenMeteoExtractor

class OpenMeteoExtractor:
    """
    Wrapper responsável por decidir qual extractor usar
    (forecast ou historical) com base na configuração recebida.

    Usa um método estático pois não precisamos manter estado:
    a única responsabilidade é instanciar e devolver o extractor correto.
    """

    @staticmethod
    def get_extractor(config):
        extractor_type = config.get("type")
        if extractor_type == "forecast":
            return ForecastOpenMeteoExtractor(config), "forecast"
        elif extractor_type == "historical":
            return HistoricalOpenMeteoExtractor(config), "historical"
        else:
            raise ValueError(f"Tipo de extractor desconhecido: {extractor_type}")
