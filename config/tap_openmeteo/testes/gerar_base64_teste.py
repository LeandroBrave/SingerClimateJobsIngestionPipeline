import json
import base64
import os

# Caminho absoluto da raiz do projeto SingerClimateJobsIngestionPipeline
# Assume que o script está em qualquer subpasta dentro de SingerClimateJobsIngestionPipeline
# Vamos subir pastas até achar a raiz pelo nome do diretório
def find_project_root(current_path, project_name="SingerClimateJobsIngestionPipeline"):
    while True:
        if os.path.basename(current_path) == project_name:
            return current_path
        parent = os.path.dirname(current_path)
        if parent == current_path:  # Chegou na raiz do sistema e não achou
            raise FileNotFoundError(f"Pasta do projeto '{project_name}' não encontrada no caminho {current_path}")
        current_path = parent

def salvar_env(base64_str, env_path):
    linha = f'CONFIG_B64="{base64_str}"\n'
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            linhas = f.readlines()
        with open(env_path, "w") as f:
            atualizou = False
            for l in linhas:
                if l.startswith("CONFIG_B64="):
                    f.write(linha)
                    atualizou = True
                else:
                    f.write(l)
            if not atualizou:
                f.write(linha)
    else:
        with open(env_path, "w") as f:
            f.write(linha)

# Nosso config hardcoded
config = {
  "type": "forecast",
  "params": {
    "latitude": -23.55,
    "longitude": -46.63,
    "hourly": "temperature_2m"
  }
}

# Converte para string JSON
config_str = json.dumps(config)

# Codifica em base64
config_base64 = base64.b64encode(config_str.encode()).decode()

print("Base64 gerado:", config_base64)

# Usa o caminho do script atual para buscar a raiz
current_dir = os.path.abspath(os.path.dirname(__file__))
root_path = find_project_root(current_dir)

# Caminho do .env na raiz
env_path = os.path.join(root_path, ".env")

salvar_env(config_base64, env_path)
print(f".env atualizado em: {env_path}")