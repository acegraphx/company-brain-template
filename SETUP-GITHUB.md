# Nastavení GitHubu

## Nejjednodušší cesta: nastaví to agent

Šéf (správce organizace na GitHubu) napíše svému Hermesovi:

> Založ v naší organizaci <název organizace> na GitHubu soukromé repo company-brain ze šablony acegraphx/company-brain-template a nastav ho podle jeho SETUP-GITHUB.md. Vlastníky oblastí nastav na konkrétní lidi místo týmů: <GitHub jméno šéfa> rozhodnutí, produkt, zakázky a pravidla, <GitHub jméno hlavního vývojáře> architektura a runbooky. Zapni kontrolu brain-check a ochranu hlavní větve. Nejdřív mi ukaž, co přesně uděláš.

Co k tomu agent potřebuje: GitHub CLI přihlášené účtem správce organizace (`gh auth login`) a plán Team nebo vyšší (ochrana větví v soukromém repu). Na zapnutí kontroly brain-check si řekne o oprávnění workflow (`gh auth refresh -s workflow`), to šéf potvrdí v prohlížeči.

### Postup pro agenta

1. `gh repo create <ORG>/company-brain --private --template acegraphx/company-brain-template --clone`
2. Všude nahradit `@ORG/<tým>` GitHub jménem vlastníka podle zadání (`.github/CODEOWNERS`, `kb/ownership.md`, `templates/`, `README.md`, `AGENTS.md`) a zbylé `ORG` názvem organizace. `python3 tools/brain_check.py --write-index` musí skončit bez chyb (potřebuje PyYAML).
3. Přesunout `tools/github-workflows/brain-check.yml` do `.github/workflows/`, commit a push (vyžaduje oprávnění workflow).
4. `gh repo edit <ORG>/company-brain --enable-merge-commit --enable-squash-merge=false --enable-rebase-merge=false --delete-branch-on-merge`
5. Ochrana hlavní větve jako ruleset (`gh api -X POST repos/<ORG>/company-brain/rulesets --input ruleset.json`): pull request s jedním schválením, schválení vlastníka oblasti, zrušení starých schválení po novém pushi, schválení posledního pushe, povinná kontrola `brain-check`, žádné výjimky, zákaz force push a mazání větve. Vzor `ruleset.json` je v `tools/github-ruleset.json`.
6. Zkouška: přímý push do `main` musí selhat. Pak shrnout šéfovi, co je nastavené.

## Ruční checklist (reference)

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
