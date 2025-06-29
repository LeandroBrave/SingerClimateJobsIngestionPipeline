# 🚀 SingerClimateJobsPipeline
Pipeline completo de ingestão e transformação usando Singer, Python, Meltano e dbt

## 📌 Objetivo

Construir um pipeline completo de ingestão e transformação de dados públicos, aplicando boas práticas de engenharia de dados:
- Ingestão de múltiplas fontes (APIs públicas)
- Armazenamento raw no S3
- Transformações com dbt no Snowflake
- Análise do impacto do clima sobre os índices de empregabilidade e desemprego

Este repo, contudo, conterá apenas o projeto singer-python.
O repo DBT para transformação um repo para exibir as analises serão referenciados aqui em breve.

---

## 🔍 Fontes de dados utilizadas

### 🌦️ Open-Meteo
API pública que fornece dados climáticos:
- **Forecast**: previsão para os próximos dias
- **Historical**: histórico climático por cidade

Campos principais:
- Temperatura, precipitação, velocidade do vento
- Latitude/longitude, cidade, data/hora
- Código de tipo de clima

---

### 🧑‍💼 CAGED (**Cadastro Geral de Empregados e Desempregados**)
Banco de dados do Ministério do Trabalho do Brasil:
- **Movimentação**: admissões e desligamentos mensais
- **Estoque**: quantidade total de vínculos ativos por mês

Campos principais:
- Ano/mês, município, setor, quantidade de vínculos, tipo de movimentação, faixa etária, sexo

---

## 🧠 Pergunta de negócio

> O clima influencia o índice de empregabilidade ou desemprego em determinadas regiões ou setores?

Vamos consolidar e analisar dados climáticos com dados de emprego para descobrir se há relação.

---

## 🧰 Arquitetura do projeto

- Ingestão: Meltano + Singer taps (open-meteo e caged) → target S3
- Armazenamento: dados raw no S3 (parquet ou JSONL)
- Transformação: dbt no Snowflake **(em breve link do repo do dbt)**
- Modelagem:
  - `stg_weather` → unifica dados forecast e histórico
  - `stg_caged` → unifica movimentação e estoque
  - `fct_emprego_clima` → integra clima e emprego por cidade/mês
- Visualização/Análise: dashboards ou notebooks **(em breve link do repo de analytics)**

---

## 🧪 Tecnologias

- Python
- Singer + Meltano (ETL/ELT)
- AWS S3 (data lake raw zone)
- Snowflake (data warehouse)
- dbt (transformação e modelagem)
- Opcional: Streamlit ou Metabase para análise final
  
---


> Projeto de portfólio para demonstrar habilidades em engenharia de dados: ingestão, transformação, modelagem e análise integrada.
