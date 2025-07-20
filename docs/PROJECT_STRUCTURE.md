# 📂 Estrutura do Projeto: SingerClimateJobsIngestionPipeline

Abaixo segue a estrutura física do projeto, com índices em cada ponto.  
Na seção seguinte, explico **em detalhes** o propósito de cada pasta e arquivo.

---

## 📦 Visão geral da estrutura

```plaintext
SingerClimateJobsIngestionPipeline/
├── .meltano/                            # [1]
├── common/                              # [2]
│   ├── singer_emitter.py
│   ├── requests_client.py
│   └── base_client.py
├── config/                              # [3]
│   └── tap_openmeteo/
│       └── gerar_base64_teste.py
├── output/                              # [4]
├── plugins/                             # [5]
│   └── taps/
│       └── tap_openmeteo/               # [5.1]
│           ├── tap_openmeteo/           # [5.1.1]
│           │   ├── __init__.py
│           │   ├── main.py
│           │   ├── singer/              # [5.1.1.1]
│           │   │   └── openmeteo_singer.py
│           │   ├── extractors/          # [5.1.1.2]
│           │   │   ├── openmeteo_extractor.py
│           │   │   ├── forecast_openmeteo_extractor.py
│           │   │   └── archive_openmeteo_extractor.py
│           │   ├── catalog/             # [5.1.1.3]
│           │   │   └── openmeteo_catalog.json
│           └── setup.py
├── .gitignore
├── meltano.yml                          # [6]
├── README.md
├── requirements.txt
└── docs/                                # [7]
    ├── PROJECT_STRUCTURE.md
    ├── WALKTHROUGH.md
    └── DEPLOY.md
```

---

## 📝 **Descrição das Principais Pastas e Arquivos**


[1] .meltano/

Pasta gerada pelo próprio Meltano, onde ficam dados internos como runs, estados (state), logs de execução etc.
⚠️ Essa pasta geralmente fica no .gitignore, pois é recriada durante o meltano install ou primeiro run.
Dificilmente há necessidade de se preocupar ou interagir com ela, mas caso precise, eu explico no doc de deploy.


[2] common/

Aqui estão os scripts utilitários compartilhados.
Exemplo: singer_emitter.py, que contém funções "core" do padrão Singer (emissão de record, de schema etc).


[3] config/

Arquivos de configuração (setup), ou testes.
Exemplo: gerar_base64_teste.py 


[4] output/

Pasta para armazenar logs, arquivos temporários ou saídas geradas pela execução da tap.
Mantemos a pasta no repositório (mas ignoramos os arquivos internos no .gitignore).


[5] plugins/taps/

Local onde ficam nossos taps Singer desenvolvidos manualmente.

[5.1] tap_openmeteo/

Pasta principal do tap que consulta a API Open-Meteo.

[5.1.1] tap_openmeteo/

Código Python do tap em si, organizado por responsabilidades.

    main.py: ponto de entrada (usa click para parsear args e rodar a tap).

    __init__.py: arquivo de inicialização do módulo.

    singer/: helpers para emitir dados no formato Singer.

    extractors/: classes responsáveis por extrair dados da API (forecast, historical etc).

    catalog/: schemas e catalog.json que define as streams.

[5.1.1.1] singer/openmeteo_singer.py

Runner da tap: transforma dados da extração em registros Singer.

[5.1.1.2] extractors/

Dividimos em arquivos separados para diferentes tipos de extração:

    forecast_openmeteo_extractor.py → previsão

    historical_openmeteo_extractor.py → histórico

    openmeteo_extractor.py → decide qual extractor usar com base no config

[5.1.1.3] catalog/

Contém openmeteo_catalog.json que define a(s) stream(s) disponíveis e seu schema.

[6] meltano.yml

Configuração principal do Meltano, onde registramos taps, targets, variantes de execução etc.

[7] docs/

Documentação do projeto:

    PROJECT_STRUCTURE.md (este arquivo)

    WALKTHROUGH.md: passo a passo do código, arquitetura e motivação.

    DEPLOY.md: instruções para instalar dependências, rodar localmente e testar.

✅ Como Usar Essa Estrutura

Essa organização ajuda a manter claro:

    Separação entre lógica, config e documentação.

    Plugins isolados do restante do projeto.

    Facilidade para testes e evolução futura.

    Em caso de dúvidas, veja o WALKTHROUGH.md para um tour guiado pelos scripts e fluxo da ingestão.

📌 ## Voltar / Navegar

- 🏗️ [Estrutura do projeto (Este Documento)](#📂-estrutura-do-projeto-singerclimatejobsingestionpipeline)  
  Explicação detalhada da organização de pastas, módulos e arquivos.

- 🔍 [Walkthrough (WALKTHROUGH.md)](WALKTHROUGH.md)  
  Um tour guiado pelo código, descrevendo a lógica interna e como tudo se conecta.

- 🚀 [Deploy e execução (DEPLOY.md)](DEPLOY.md)  
  Como preparar o ambiente, instalar dependências e executar localmente.

- 🏠 [Voltar ao README principal](../README.md)
