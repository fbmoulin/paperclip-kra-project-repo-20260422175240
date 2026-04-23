# Paperclip Kratos Research Automation

MVP para pesquisa automatizada de vídeos no YouTube, formação de fontes para NotebookLM e geração de insumos para conteúdo.

## Objetivo

Automatizar um pipeline que:
- recebe um tema
- pesquisa vídeos relevantes no YouTube
- organiza metadados e fontes
- prepara resumos e notas para NotebookLM
- gera insumos para posts, artigos, tutoriais e projetos

## Escopo do MVP

O MVP atual entrega:
- estrutura inicial do projeto
- configuração por arquivo JSON
- CLI para executar o pipeline
- etapas de:
  - ingestão de tópicos
  - descoberta de fontes
  - curadoria inicial
  - export de resultados em Markdown e JSON

## Estrutura

```text
src/
  paperclip_kratos/
    cli.py
    config.py
    models.py
    pipeline.py
    providers/
      youtube.py
    exporters/
      markdown.py
      notebooklm.py
configs/
  topics.example.json
output/
  .gitkeep
prompts/
  content-brief.md
```

## Fluxo proposto

1. Definir tema e objetivo
2. Buscar vídeos candidatos
3. Normalizar metadados
4. Aplicar score inicial de relevância
5. Exportar:
   - JSON estruturado
   - Markdown para revisão humana
   - pacote de fontes para NotebookLM

## Uso

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m paperclip_kratos.cli run --config configs/topics.example.json
```

## Saídas

Arquivos gerados em `output/`:
- `research-report.json`
- `research-report.md`
- `notebooklm-sources.md`

## Próximos passos

- integrar busca real em YouTube Data API
- integrar transcript extraction
- adicionar score por autoridade do canal
- gerar briefs de Instagram, Linkding e artigos
- adicionar persistência e histórico de execuções
