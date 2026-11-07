# SCHEMA: typy stránek a povinná pole

Platí pro soubory v `kb/` kromě `AGENTS.md` a `README.md`. Kontrolu dělá `tools/brain_check.py` lokálně i v CI.

## Typy (`type`)

| type | kam (konvence) | povolený status | k čemu |
|---|---|---|---|
| concept | kb/architecture/, kb/product/, kb/projects/ | official, deprecated | pojem nebo popis části systému |
| runbook | kb/runbooks/ | official, deprecated | postup: build, release, nasazení, obnova |
| known-issue | kb/product/ | official, deprecated | známá chyba + workaround, bez doslovného textu zákazníků |
| faq | kb/product/ | official, deprecated | opakující se otázka a ověřená odpověď |
| glossary | kb/glossary.md | official, deprecated | pojmy s odkazem na zdroj |
| decision | kb/decisions/ | proposed, confirmed, superseded | jedno rozhodnutí = jeden soubor |

Umístění podle složky skript neověřuje; je to konvence.

## Povinná pole (všechny typy)

`id`, `title`, `type`, `status`, `owner`, `sensitivity`, `sources`, `confidence`, `created`, `updated`, `review_by`

- `id`: stabilní a jedinečný v repu. Nemění se při přejmenování souboru.
- `owner`: tým z `.github/CODEOWNERS`, např. `"@firma/tech-leads"`.
- `sensitivity`: v této šabloně jediná povolená hodnota je `internal`.
- `sources`: neprázdný seznam položek s `kind` a `ref`. `kind: customer-report` musí mít `trust: untrusted`. Stránka, jejíž všechny zdroje jsou nedůvěryhodné, nesmí mít `confidence: high`.
- `confidence`: `high`, `medium`, `low`. Konvence: `high` jen s ověřeným zdrojem v kódu nebo reprodukcí.
- `created`, `updated`, `review_by`: datum `RRRR-MM-DD`. Po `review_by` skript vypíše varování.

Doporučené hodnoty `kind`: `code`, `github-issue`, `github-pr`, `doc`, `customer-report`, `meeting` (odkaz s časem, ne text).

## Rozhodnutí (`type: decision`) navíc

- `decision`, `decided_by`, `decided_on`, `participants`, `meeting` (s `date` a `transcript`).
- `transcript` je odkaz s časem, např. `meetings-raw:2026-11-14-porada#00:41:20`. Text přepisu do repa nepatří.
- `status: proposed` do `main` neprojde. Nejdřív `confirmed`, potvrzuje účastník schůzky.
- `superseded` vyžaduje `superseded_by`. Nový záznam má `supersedes`.
- Každá položka `action_items` má `what` a `who`.

## Co skript hlídá

- chybějící frontmatter nebo pole, hodnoty výčtů, formát datumů
- vlastník je v CODEOWNERS
- zdroje a `trust` u zákaznických zdrojů; `confidence` vůči zdrojům
- vzory: e-mail, telefon, privátní klíč, GitHub token, API klíč, „ignore previous instructions“ a česká obdoba, „system prompt“, HTML komentář
- `index.md` odpovídá stránkám
- s `--commits origin/main`: commit s trailerem `Agent:` musí mít `Source:` a `Co-authored-by:`

Vzory jsou jednoduché regulární výrazy. Nejsou to plnohodnotný skener tajemství. Hlavní pojistka je člověk v review.

Tvar stránky je v `templates/`. `index.md` je generovaný, neupravuj ho ručně.
