# CLAUDE.md

Dette dokument instruerer Claude Code i workflow for Publishing Agent (MCP Server).

Sprog: dansk
Tone: skarp, direkte, forretningsorienteret.

## Workflow

1. Når bruger skriver en ny idé, brug værktøjet:
   - Svar med spørgsmål der skærper idéen: målgruppe, problem, budskab, format.
   - Gem dialogen i `conversation`-felt i idé-objekt.

2. Når bruger skriver "gem ide",
   - kald endpoint `/save_idea` med:
     - `title`, `subtitle`, `bullets`, `raw_idea`, `conversation`, `status` ('ny').

3. Når bruger skriver "hent ide #<id>" eller "get idea" i en senere omgang,
   - kald `/get_idea/{id}` og fortsæt dialogen med den fulde samtale.

4. Ved opdatering: `update_idea/{id}` med de ændrede felter.

5. For sletning: `delete_idea/{id}`.

## Tool-kald

- `save_idea`: opret idé
- `get_ideas?status=<status>`: hent filtreret liste
- `get_idea/<id>`: hent ene idé med samtalehistorik
- `update_idea/<id>`: opdater idé (title, bullets, status, conversation)
- `delete_idea/<id>`: slet idé

## Status (idé)

- ny
- in-progress
- afventer
- klar

## Formidlingstips til Claude

- Brug cases:
  - idéudvikling og brainstorming
  - kvantificer input som bullet points
  - hold alle beskeder i `conversation` så status og kontekst bevares

## Server setup

- Start med `python -m uvicorn server:app --reload`.
- Alternativt kan gavnes `poetry`/`pip` med `fastapi`, `uvicorn`.
