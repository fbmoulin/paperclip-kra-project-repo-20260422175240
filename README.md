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
- integração real com YouTube Data API quando `YOUTUBE_API_KEY` estiver configurada
- fallback seguro para placeholders quando a chave não estiver configurada
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
export PYTHONPATH=src
python -m paperclip_kratos.cli run --config configs/topics.example.json
```

### YouTube Data API

Para busca real, configure:

```bash
export YOUTUBE_API_KEY="sua-chave-aqui"
```

Sem isso, o pipeline gera fontes placeholder para você validar a arquitetura e os exports.

## Saídas

Arquivos gerados em `output/`:
- `research-report.json`
- `research-report.md`
- `notebooklm-sources.md`

## Próximos passos

- integrar transcript extraction
- adicionar score por autoridade do canal e recência por nicho
- gerar briefs de Instagram, Linkding e artigos
- adicionar persistência e histórico de execuções
- incluir filtros por idioma, duração e data
