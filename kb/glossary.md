---
id: kb-glossary-0001
title: "Slovníček pojmů"
type: glossary
status: official
owner: "@ORG/brain-maintainers"
sensitivity: internal
sources:
  - kind: doc
    ref: "git-interpret-trailers(1); místně: git help interpret-trailers"
confidence: high
created: 2026-11-07
updated: 2026-11-07
review_by: 2027-05-07
supersedes: []
contested: false
---

# Slovníček pojmů

Ukázkové záznamy. Nahraď je pojmy své firmy a u každého uveď zdroj.

## Pull request (PR)

Návrh změny ve větvi, který se dostane do `main` až po schválení a sloučení. Jediná cesta, jak změnit obsah mozku.
Zdroj: AGENTS.md, pravidla 2 a 3.

## Trailer commitu

Řádek na konci zprávy commitu ve tvaru `Klíč: hodnota`, např. `Source: <odkaz>`. Git ho čte např. příkazem `git log --format='%(trailers)'`.
Zdroj: git-interpret-trailers(1).
