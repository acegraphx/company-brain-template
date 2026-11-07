# Nastavení GitHubu (checklist)

Den předem projdi na vlastní organizaci. Názvy voleb v GitHub UI se mění. Položky označené [ověřit] zkontroluj na místě.

## Předpoklady

- [ ] Organizace na plánu Team nebo vyšším. Podle návrhu bez něj privátní repo nemá ochranu větví ani CODEOWNERS [ověřit aktuální podmínky].
- [ ] Owner organizace je na místě. Všichni účastníci mají účet v organizaci.
- [ ] Týmy existují: `brain-maintainers` a vlastníci oblastí (`tech-leads`, `product-owners`, `project-leads`), s právem zápisu.

## Repozitář

- [ ] Nahraď `ORG` v `.github/CODEOWNERS`, `kb/glossary.md`, `kb/ownership.md`, `AGENTS.md`, `README.md` a `templates/`. Kontrola: `grep -rn "ORG/" .`
- [ ] Repo je privátní.
- [ ] Settings → General → Pull Requests: povolit „Create a merge commit“, vypnout squash [ověřit názvy voleb].
- [ ] Lokálně: `python3 tools/brain_check.py` skončí bez chyb.

## Ochrana `main` (ruleset nebo branch protection)

- [ ] Require a pull request before merging, 1 schválení.
- [ ] Require review from Code Owners.
- [ ] Dismiss stale pull request approvals when new commits are pushed.
- [ ] Require approval of the most recent reviewable push.
- [ ] Require status checks to pass: vyber `brain-check`. Check se v seznamu objeví až po prvním běhu workflow [ověřit].
- [ ] Do not allow bypassing the above settings.
- [ ] Force push a mazání větve zakázané (výchozí stav).
- [ ] Autor PR nemůže schválit vlastní PR. Ověř zkušebním PR se dvěma účty [ověřit].

## Zkouška den předem

- [ ] Přímý push do `main` z účtu bez správcovských práv selže.
- [ ] PR s falešným tokenem (`ghp_` + 36 znaků) shodí `brain-check`.
- [ ] PR bez schválení nejde sloučit.
- [ ] Změna v `kb/architecture/` vyžaduje schválení vlastníka [ověřit].

## Workflow (zapnout v novém repu)

- [ ] Kontrola `brain-check` je v šabloně uložená jako `tools/github-workflows/brain-check.yml`, ne v `.github/workflows/`, aby šla šablona nahrát i tokenem bez oprávnění `workflow`. V novém repu ji zapni jedním ze dvou způsobů:
  - v GitHubu: Add file → Create new file → název `.github/workflows/brain-check.yml` → vložit obsah souboru `tools/github-workflows/brain-check.yml` → commit přes PR;
  - lokálně: `mkdir -p .github/workflows && git mv tools/github-workflows/brain-check.yml .github/workflows/` a push účtem nebo tokenem s oprávněním `workflow`.
- [ ] Po prvním běhu se check `brain-check` objeví v nastavení ochrany `main` (viz výše).
- [ ] Workflow nebyl otestován na GitHubu. Lokálně je otestován jen skript. Ověř, že `actions/checkout@v6` a `pip install pyyaml` na hosted runneru fungují [ověřit].
