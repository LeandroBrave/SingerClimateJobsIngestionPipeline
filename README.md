# 🚀 SingerClimateJobsPipeline
Pipeline completo de ingestão e transformação usando Singer, Python, Meltano e dbt

# 📝 Planejamento
Parte 1 - Ingestão batch
Este repo é a parte 1 de uma série composta por 4 repositórios.
Em breve a disponibilização da parte 2, um repo de ingestão de big data com Pyspark
Em seguida a disponibilização da parte 3, um repo de transformação com DBT.
Por fim, a disponibilização da parte 4, algo simples para expor a parte de analytics.

## 📌 Objetivo

Construir um pipeline completo de ingestão e transformação de dados públicos, aplicando boas práticas de engenharia de dados:
- Ingestão de múltiplas fontes (APIs públicas e bancos de dados)
- Armazenamento raw no S3
- Transformações com dbt no Snowflake
- Análise do impacto do clima sobre os índices de empregabilidade e desemprego

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

### 🗄️ Banco de Dados
Dados já coletados e armazenados em um banco postgres

- O teor do dado ainda será definido

Campos e tabelas principais:

    A serem definidos.

---

## 🧠 Pergunta de negócio

> O clima influencia o índice de empregabilidade ou desemprego em determinadas regiões ou setores?

Vamos consolidar e analisar dados climáticos com dados de emprego para descobrir se há relação.

---

## 🧰 Arquitetura do projeto

- Ingestão 1: Meltano + Singer taps (open-meteo, caged e postgres) → target S3
- Ingestão 2: Pyspark (detalhes ainda a serem definidos)
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
- Spark
- Singer + Meltano (ETL/ELT)
- AWS S3 (data lake raw zone)
- Snowflake (data warehouse)
- dbt (transformação e modelagem)
- Sujeito a alterações: Streamlit ou Metabase para análise final
  
---


> Projeto de portfólio para demonstrar habilidades em engenharia de dados: ingestão, transformação, modelagem e análise integrada.
