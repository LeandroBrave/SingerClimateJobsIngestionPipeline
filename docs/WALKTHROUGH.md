# 📖 Walkthrough do Projeto

Farei referências a pastas e arquivos do projeto durante esta documentação.  
Para ter um melhor contexto sobre a organização do projeto, estrutura física e a finalidade de cada pasta, consulte o arquivo [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md).

---

## ✅ Visão geral

Este walkthrough explica, passo a passo, como a tap funciona:
- Como ela extrai dados via HTTP
- Como aplica o padrão **Singer** para emitir os dados
- Como usa o catálogo para garantir que tudo saia com o formato correto
- E como a `main.py` integra tudo isso, oferecendo diferentes modos de execução

---

## 🧩 **Ponto 1 – As Requests HTTP**

A primeira etapa de uma tap é **extrair os dados da fonte**.  
No nosso caso, os dados vêm da API **Open-Meteo** e para organizar isso usamos **3 camadas**:

---

### 🛠️ 1️⃣ `common/requests_client.py`

Este módulo é o mais **genérico** possível.  
Ele sabe apenas:
- Fazer uma requisição HTTP (usando `requests`)
- Montar a URL completa usando base URL + endpoint + query parameters
- Retornar o `response.json()`

Essa simplicidade permite reaproveitar a mesma classe para qualquer API ou qualquer tap futura.

---

### 🧱 2️⃣ `common/base_client.py`

Um módulo genérico costuma virar um “Frankenstein” quando precisa atender necessidades muito diferentes.  
Para evitar isso, **criamos uma abstração**: `base_client.py`.

Essa abstração:
- Centraliza **como** vamos chamar a classe genérica
- Define métodos de extração padrão (ex.: `extract()`)
- Permite que taps ou extractors concretos **herdem** dela e só implementem o que for necessário para lidar com peculiaridades da API ou endpoint.

---

### 🌦️ 3️⃣ `forecast_openmeteo_extractor.py` e `historical_openmeteo_extractor.py`

Esses arquivos ficam na pasta `extractors` e **herdam** do `base_client.py`.  
Cada um é responsável por lidar com:
- O endpoint específico (`forecast` ou `historical`)
- Parametrizações próprias da requisição
- Como extrair ou filtrar os dados no `response`

Dessa forma, se quisermos consumir outro endpoint da Open-Meteo ou outra API, podemos criar outro extractor que:
- Reaproveita a base (requests_client)
- Mantém as particularidades bem isoladas

---

## 🎼 **Ponto 2 – O Singer**

Depois de extrair os dados da API, precisamos aplicar o padrão **Singer**. Aqui definimos o catálogo e construimos a lógica da tap (eu vou ficar devendo os targets, mas só por enquanto!).

---

### 📦 O que é o catálogo?

Arquivo: [`catalog/openmeteo_catalog.json`](../plugins/taps/tap_openmeteo/tap_openmeteo/catalog/openmeteo_catalog.json)

Ele descreve:
- As **streams** (ex.: `forecast`, `historical`), que são basicamente “tabelas” de dados que a tap pode expor.
- Os **schemas**, ou seja, quais campos cada stream terá, seus tipos e restrições.
- As **key_properties**, campos que servem como chave primária (essencial para deduplicação ou cargas incrementais).

---

#### 🧩 **Por que podemos ter várias streams?**

Imagine que queremos atender diferentes necessidades:
- Uma stream **full_forecast**, completa, com todos os campos e metadados.
- Uma stream **data_forecast**, só com as medidas de interesse e timestamp, mais enxuta.

Ao definir várias streams:
- A tap pode servir múltiplos consumidores sem alterar a extração base.
- Cada consumidor escolhe a stream que melhor atende sua necessidade.
- Permite evoluir, criar novas visões ou filtros sem quebrar quem já usa a tap.

No nosso projeto, hoje temos apenas a stream `forecast`, mas a arquitetura está preparada para crescer.

---

### 🛠️ `common/singer_emitter.py`

É um módulo **genérico** que implementa os métodos básicos do Singer:
- `write_schema`: emite o schema no stdout (target precisa saber qual estrutura vai chegar)
- `write_state`: emite o estado (usado para controle incremental)
- `write_record`: emite um registro individual
- `write_batch_records`: emite uma lista de registros

Qualquer tap nossa vai precisar desses métodos, então eles ficam **centralizados** aqui.

---

### 🎼 `openmeteo_singer.py`

Fica na pasta `singer` dentro da tap.

Essa classe:
- Recebe um extractor (por ex.: `forecast_openmeteo_extractor`)
- Recebe o caminho do catálogo
- Recebe o nome da stream a processar

No método `run()`:
- Extrai os dados do extractor
- Lê do catálogo qual é o schema e key_properties da stream escolhida
- Emite o schema
- Emite todos os registros extraídos (via `write_batch_records`)

---

## 🧰 **Ponto 3 – A Main**

Arquivo: [`main.py`](../plugins/taps/tap_openmeteo/tap_openmeteo/main.py)

É o **ponto de entrada** da tap.  
Usa `click` para criar uma interface de linha de comando que oferece diferentes modos de execução:

| Flag / Argumento | O que faz |
|------------------|-----------|
| `--config` (obrigatório) | Recebe um base64 com dados necessários (ex.: latitude, longitude). |
| `--catalog` | Opcional; se passado, usamos esse schema ao invés do que está na pasta catalog. |
| `--discover` | Escreve no stdout o conteúdo do catálogo (modo exploratório). |
| `--about` | Exibe um resumo sobre o projeto e os comandos disponíveis. |
| `--test_request` | Executa apenas a requisição HTTP, sem passar pelo Singer (modo debug). |

---

### ⚙️ **Fluxo resumido da execução principal**:

1. Recebe os parâmetros do usuário (CLI)
2. Se for discover ou about, responde direto e termina
3. Se for test_request, chama o extractor, faz a requisição http e imprime o resultado cru
4. Caso contrário, instancia o extractor, o runner (`openmeteo_singer.py`) e chama `run()`, que:
   - Emite o schema
   - Extrai os dados
   - Emite os records no formato Singer

---

## ✅ **Conclusão**

- Usamos abstrações para separar **lógica genérica** (common) da **lógica específica** da request.
- O catálogo permite versionar schemas e oferecer múltiplas visões dos dados.
- O padrão Singer garante compatibilidade com qualquer target que implemente Singer.
- A `main.py` organiza tudo e oferece diferentes formas de rodar e explorar a tap.

---

## 📌 **Menu de Navegação**

- 🏗️ [Estrutura do projeto (`PROJECT_STRUCTURE.md`)](PROJECT_STRUCTURE.md)  
- 🔍 [Walkthrough (este documento)](WALKTHROUGH.md)  
- 🚀 [Deploy e execução (`DEPLOY.md`)](DEPLOY.md)
- 🏠 [Voltar ao README principal](../README.md)

