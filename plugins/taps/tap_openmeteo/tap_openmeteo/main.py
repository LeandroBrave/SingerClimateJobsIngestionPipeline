import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

import base64
import json
import click
import logging
from .extractors.openmeteo_extractor import OpenMeteoExtractor
from .singer import openmeteo_singer

def do_about():
    about_info = {
        "name": "tap-openmeteo",
        "version": "0.1.0",
        "description": "Tap to extract data from Open-Meteo API",
        "author": "Leandro Valente",
        "commands": [
            {
                "name": "run_tap",
                "description": "Executa a tap completa, lendo do catalog e emitindo dados no formato Singer."
            },
            {
                "name": "do_discover",
                "description": "Exibe no stdout o catalog JSON disponível, útil para descobrir streams e schemas."
            },
            {
                "name": "do_test_request",
                "description": "Executa somente a request na API e imprime o resultado bruto, sem transformar em registros Singer."
            }
        ]
    }
    print(json.dumps(about_info, indent=2))


def do_discover(catalog_path):
    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)
    print(json.dumps(catalog, indent=2))


def do_test_request(extractor_instance):
    data = extractor_instance.extract()
    print(json.dumps(data, indent=2))


def run_tap(extractor_instance, catalog_path, stream_name):
    tap_runner = openmeteo_singer.OpenMeteoSingerRunner(extractor_instance, catalog_path, stream_name)
    tap_runner.run()

@click.command()
@click.option('--config', required=True, help='Config JSON em base64')
@click.option('--catalog', required=False, help='Caminho para o catalog JSON')
@click.option('--discover', is_flag=True, help='Imprime o catalog JSON no stdout e sai')
@click.option('--about', is_flag=True, help='Imprime metadados do projeto em JSON e sai')
@click.option('--test-request', is_flag=True, help='Testa apenas a request, sem rodar a tap completa')
def main(config, catalog, discover, about, test_request):
    logging.basicConfig(level=logging.INFO)
    logging.info("Iniciando a execução da tap_openmeteo...")

    # Se não vier, usa o padrão
    catalog_path = catalog or os.path.join(os.path.dirname(__file__), 'catalog', 'openmeteo_catalog.json')

    if config:
        try:
            decoded = base64.b64decode(config).decode('utf-8')
            config_dict = json.loads(decoded)

            extractor_instance, stream_name = OpenMeteoExtractor.get_extractor(config_dict)
        except Exception as e:
            logging.error("Erro ao decodificar config base64:", exc_info=True)
            raise
    else:
        config = ""

    if about:
        logging.info("Executando --about")
        do_about()
    elif discover:
        logging.info("Executando --discover")
        do_discover(catalog_path)
    elif test_request:
        logging.info("Executando --test-request")
        do_test_request(extractor_instance)
    else:
        logging.info(f"Executando tap completa usando catalog: {catalog_path}")
        run_tap(extractor_instance, catalog_path, stream_name)

if __name__ == '__main__':
    main()
