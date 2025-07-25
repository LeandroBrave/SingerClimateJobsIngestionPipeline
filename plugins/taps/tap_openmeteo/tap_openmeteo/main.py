import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

import base64
import json
import logging
import argparse
from .extractors.openmeteo_extractor import OpenMeteoExtractor
from .singer import openmeteo_singer
from singer import utils

CATALOG_PATH = os.path.join(os.path.dirname(__file__), 'catalog', 'openmeteo_catalog.json')

def do_about():
    about_info = {
        "name": "tap-openmeteo",
        "version": "0.1.0",
        "description": "Tap to extract data from Open-Meteo API",
        "author": "Leandro Valente",
        "commands": [
            {
                "name": "run_tap",
                "description": "Executa a tap completa, lendo do catalog e emitindo dados no formato Singer.",
                "exemplo":{
                    "Rodar apenas a tap": "meltano invoke nome_da_tap --config '$CONFIG_B64' > output/nome_do_arquivo_de_saida.log",
                    "Ou simplesmente": "meltano invoke nome_da_tap",
                    "Exemplo":"meltano invoke tap-openmeteo",

                    "Rodar a tap e o target": "meltano run nome_da_tap nome_do_target",
                    "Exemplo":"meltano run tap-openmeteo jsonl"
                }
                    
            },
            {
                "name": "do_discover",
                "description": "Exibe no stdout o catalog JSON disponível, útil para descobrir streams e schemas.",
                "exemplo":{
                    "Comando":"meltano invoke tap-openmeteo --config '' --discover"
                }
            },
            {
                "name": "do_test_request",
                "description": "Executa somente a request na API e imprime o resultado bruto, sem transformar em registros Singer.",
                "exemplo":{
                    "Comando":"meltano invoke tap-openmeteo --config '$CONFIG_B64' --test-request"
                }
            }
        ]
    }
    print(json.dumps(about_info, indent=2))


def do_discover(catalog_path):
    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)
    return catalog

def do_test_request(extractor_instance):
    data = extractor_instance.extract()
    print(json.dumps(data, indent=2))


def run_tap(extractor_instance, catalog, stream_name):
    tap_runner = openmeteo_singer.OpenMeteoSingerRunner(extractor_instance, catalog, stream_name)
    tap_runner.run()

def load_config(required_keys):
    # no meltano.yml temos o atributo settings da nossa tap
    # ele indica que o config vai assumir o valor da variável de ambiente $CONFIG_B64 (.env)
    # e pode ser capturada pelo método parse_args da utils do singer, conforme abaixo
    # ele também pega o valor do $CONFIG_B64 e encapsula em uma string json
    try:
        args = utils.parse_args(required_config_keys=required_keys)
        logging.info("Valor do config:")
        logging.info(args.config)
        return args.config
    except Exception:
        logging.warning("Falha ao parsear args. Tentando pegar do ambiente...")

        env_config = os.environ.get("CONFIG_B64") #caso o config venha via linha de comando
        if not env_config:
            raise RuntimeError("Configuração não encontrada em args nem no ambiente.")

        # monta o dicionário com a mesma estrutura que parse_args retornaria
        return {"config": env_config}

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Iniciando a execução da tap_openmeteo...")

    #adicionando nossas tags CLI customizadas
    parser = argparse.ArgumentParser(add_help=False)  # Sem help automático para evitar conflito
    parser.add_argument("--about", action="store_true", help="Exibe informações da tap")
    parser.add_argument("--discover", action="store_true", help="Executa teste na API")
    parser.add_argument("--test-request", action="store_true", help="Executa teste na API")
    known_args, _ = parser.parse_known_args()
    
    # Remove os argumentos customizados antes de passar para singer.utils
    sys.argv = [arg for arg in sys.argv if arg not in ["--about", "--test-request", "--discover"]]

    #capturando o config parametrizado ou passado via CLI
    config = load_config(required_keys=["config"])

    if config:
        try:
            decoded = base64.b64decode(config["config"]).decode('utf-8')
            config_dict = json.loads(decoded)

            extractor_instance, stream_name = OpenMeteoExtractor.get_extractor(config_dict)
        except Exception as e:
            logging.error("Erro ao decodificar config base64:", exc_info=True)
            raise

    if known_args.about:
        logging.info("Executando --about")
        do_about()
    elif known_args.discover:
        logging.info("Executando --discover")
        print(json.dumps(do_discover(CATALOG_PATH), indent=2))
    elif known_args.test_request:
        logging.info("Executando --test-request")
        do_test_request(extractor_instance)
    else:
        logging.info(f"Executando tap completa usando catalog: {CATALOG_PATH}")
        run_tap(extractor_instance, do_discover(CATALOG_PATH), stream_name)

if __name__ == '__main__':
    main()