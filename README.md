# 🚀 SingerClimateJobsPipeline
Pipeline completo de ingestão batch com Singer, Python e Meltano.  
Este repositório faz parte de uma **série de 4 repositórios separados** que, juntos, compõem um pipeline completo de engenharia de dados.

---

## 📝 Planejamento

**Estrutura da série de repositórios:**

- ✅ **Parte 1 (este repositório)**: Ingestão batch com Singer + Meltano
- 🛠 **Parte 2 (em desenvolvimento, outro repositório)**: Ingestão big data com PySpark
- 📦 **Parte 3 (a ser entregue em outro repositório)**: Transformação e modelagem com dbt
- 📊 **Parte 4 (a ser entregue em outro repositório)**: Analytics e visualização (ex: dashboards ou notebooks)

Cada etapa ficará em um repositório separado para manter a arquitetura limpa e modular.

---

## 📌 Objetivo

Construir um pipeline completo de ingestão e transformação de dados públicos, aplicando boas práticas de engenharia de dados:
- Ingestão de múltiplas fontes (APIs públicas, banco de dados e arquivos)
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

### 🗄️ Banco de Dados (PostgreSQL)
Ingestão via tap própria lendo tabelas de um banco PostgreSQL.
- O teor e schema dos dados ainda serão definidos.

---

## 🧠 Pergunta de negócio

> O clima influencia o índice de empregabilidade ou desemprego em determinadas regiões ou setores?

Vamos consolidar e analisar dados climáticos junto com dados de emprego para investigar se existe correlação.

---

## 🧰 Arquitetura geral

- **Ingestão 1 (este repositório)**: Meltano + Singer taps (open-meteo, caged e postgres) → target S3
- **Ingestão 2 (outro repositório, em desenvolvimento)**: PySpark para extrações massivas e paralelas
- **Armazenamento**: dados raw no S3 (parquet ou JSONL)
- **Transformação (outro repositório, a ser entregue)**: dbt no Snowflake
- **Modelagem (outro repositório, a ser entregue)**:
  - `stg_weather`: unifica dados forecast e histórico
  - `stg_caged`: unifica movimentação e estoque
  - `fct_emprego_clima`: integra clima e emprego por cidade/mês
- **Visualização/Analytics (outro repositório, a ser entregue)**: dashboards ou notebooks

---

## 🧪 Tecnologias

- Python
- Singer + Meltano (ETL/ELT)
- Spark (ingestão massiva, parte 2)
- AWS S3 (data lake raw zone)
- Snowflake (data warehouse)
- dbt (transformação e modelagem)
- Streamlit ou Metabase (visualização final, a definir)

---

> Projeto de portfólio para demonstrar habilidades em engenharia de dados: ingestão, transformação, modelagem e análise integrada.

---

## 📚 Documentação Técnica

- 🔍 [Walkthrough (WALKTHROUGH.md)](docs/WALKTHROUGH.md)  
  Um tour guiado pelo código, descrevendo a lógica interna e como tudo se conecta.

- 🏗️ [Estrutura do projeto (PROJECT_STRUCTURE.md)](docs/PROJECT_STRUCTURE.md)  
  Explicação detalhada da organização de pastas, módulos e arquivos.

- 🚀 [Deploy e execução (DEPLOY.md)](docs/DEPLOY.md)  
  Como preparar o ambiente, instalar dependências e executar localmente.

---

## 🛠️ Fluxo de desenvolvimento

Este repositório usa `pre-commit` localmente e GitHub Actions para CI.

### Local

1. Crie um ambiente Python e instale dependências:

```bash
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

2. Ative o hook do `pre-commit`:

```bash
pre-commit install
```

3. Antes de commitar, o `pre-commit` rodará automaticamente e bloqueará commits com problemas de formatação ou lint.

### CI no GitHub

- Um workflow em `.github/workflows/python-ci.yml` roda em `push` e `pull_request` para `main` e `dev`.
- Ele instala dependências, roda `pre-commit` em todos os arquivos e faz validação de sintaxe Python.

### Comandos úteis

```bash
git checkout dev
# editar código
git add .
git commit -m "feat: ..."
git push origin dev
```

Se você ainda não tiver criado a branch `dev` localmente, use:

```bash
git checkout -b dev origin/main
```
