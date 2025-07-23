# 🚀 Deploy e exec local

Este guia mostra passo a passo como clonar, instalar e rodar o projeto **SingerClimateJobsIngestionPipeline** localmente.

> ✅ **Observação:** recomendamos usar o **Git Bash** (ou terminal compatível), pois os comandos abaixo estão escritos no formato **bash**.

---

## 📦 Passo a passo de instalação

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/LeandroBrave/SingerClimateJobsIngestionPipeline.git
```

### 2️⃣ Usar o Git Bash

Os comandos deste tutorial estão no formato bash, que funcionam melhor no Git Bash (Windows) ou qualquer terminal Unix-like.

---

### 3️⃣ Criar e ativar um ambiente virtual

```bash
python -m venv venv
source venv/Scripts/activate  # Windows (Git Bash)
```

### 4️⃣ Navegar até a pasta principal do projeto

```bash
cd SingerClimateJobsIngestionPipeline
```

### 5️⃣ Instalar as dependências
```bash
Tente instalar todas de uma vez:

pip install -r requirements.txt

Se der problema, instale uma a uma:

pip install click
pip install requests
pip install singer-python
pip install meltano==3.7.8
```

### 6️⃣ Gerar o arquivo de configuração
```bash
Dentro da pasta config/tap_openmeteo/ temos um script para gerar a configuração codificada em base64.

Execute:

python config/tap_openmeteo/gerar_base64_teste.py

Ou simplesmente abra o arquivo e execute usando sua IDE preferida.

OBS:
Por volta da linha 72, há esse trecho:
# Converte para string JSON
config_str = json.dumps(escolherStream('archive')) #Mude aqui entre archive ou forecast, 
                                                      #para produzir diferentes stups de parametrização
é aqui que vc define se o seu config do .env recebe uma parametização default do forecast ou archive 
apenas mudando esse parâmetro                                                      
```

### 7️⃣ Exportar a variável de ambiente
```bash
No bash / Git Bash:

source .env
```

### 8️⃣ Instalar a tap e o target
```bash
meltano install extractor tap-openmeteo

depois

meltano install loader target-jsonlS

esses installs são puramente por desencargo. O seu meltano.yml já estárá configurado vindo do repositorio remoto.
```

### 9️⃣ Opções de execução
```bash
meltano invoke tap-openmeteo --about

🧩 Entendendo as opções de execução

Depois que tudo estiver configurado, você pode executar a tap de várias formas para diferentes finalidades:
📍 --about

Exibe informações gerais do projeto:

    Nome, versão, descrição

    Comandos disponíveis

    Exemplos práticos

Exemplo:

meltano invoke tap-openmeteo --about

🔍 --discover

Mostra no terminal o catálogo JSON (schemas e streams) que a tap oferece.
Útil para explorar rapidamente quais estruturas de dados estão disponíveis.

meltano invoke tap-openmeteo --discover

🧪 --test_request

Executa apenas a requisição HTTP, sem transformar os dados no formato Singer.
Ótimo para debug ou exploração da resposta bruta da API.

meltano invoke tap-openmeteo --config "seu base64" --test_request
ou simplesmente:
meltano invoke tap-openmeteo --test_request (para usar o base64 do .env)

▶️ Execução completa da tap

Executa todo o fluxo:

    Consulta a API

    Emite o schema (definido no catálogo)

    Emite os registros extraídos no formato Singer

meltano invoke tap-openmeteo --config "seu base64" > output/forecast_tap_run.log
ou simplesmente
meltano invoke tap-openmeteo > output/forecast_tap_run.log

    Isso gera um arquivo .log com todas as mensagens Singer (schema + records).

É possível executar a tap com o extrator json, com o comando:
 meltano run tap-openmeteo target-jsonl (usando o config do .env)
 um json será criado na pasta output
```

✅ Resumo

Essa organização permite que você:

    Visualize o catálogo (--discover)

    Teste rapidamente a API (--test_request)

    Execute a ingestão completa (stdout)

    Veja um help com exemplos (--about)

📌 Voltar / Navegar

- 🏗️ [Estrutura do projeto (PROJECT_STRUCTURE)](PROJECT_STRUCTURE.md)  
  Explicação detalhada da organização de pastas, módulos e arquivos.

- 🔍 [Walkthrough (WALKTHROUGH.md)](WALKTHROUGH.md)  
  Um tour guiado pelo código, descrevendo a lógica interna e como tudo se conecta.

- 🚀 [Deploy e execução (Este Documento)](#🚀-Deploy-e-exec-local)  
  Um tour guiado pelo código, descrevendo a lógica interna e como tudo se conecta.

- 🏠 [Voltar ao README principal](../README.md)