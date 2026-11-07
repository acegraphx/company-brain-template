# TESTED: ověření brain_check.py a šablony

Test proběhl lokálně 7. 11. 2026 v dočasném repu (`scratch/skoleni-hermes/materials-work/brain-test-run`), bez zápisu na GitHub.

Prostředí: git 2.43.0; `/usr/bin/python3` s PyYAML 6.0.1; skript je identický s Přílohou A návrhu (`cmp` OK).
Pozor: `python3` v prostředí Hermes (venv) nemá PyYAML. Skript pak skončí s `Chybí PyYAML: pip install pyyaml` (zachyceno při testu). Na školení: `pip install pyyaml` před prvním během.

Výsledek:
- dobrá stránka + commit s trailery `Agent:`, `Source:`, `Co-authored-by:` → **prošlo** (rc=0)
- špatné stránky (bez zdroje, falešný token, nepotvrzené rozhodnutí) → **selhalo** (rc=1), tři hlášky s názvem souboru
- commit agenta bez `Source:` a `Co-authored-by:` → **selhalo** (rc=1)

Redakce: falešný token (`ghp_` + 36 znaků) je v tomto záznamu zredigován. Skript ho vypisuje celý. Záměrně se nepíše do repa, protože GitHub ho může vyhodnotit jako únik tajemství.

Příkazy a výstupy (zkráceno jen o prázdné řádky):

```text
$ git init -q -b main
# rc=0
(bez výstupu)

$ git -c user.name=Šablona test -c user.email=sablona-test@example.com add -A
# rc=0
(bez výstupu)

$ git -c user.name=... commit -m 'init: šablona company-brain'
# rc=0
(bez výstupu)

$ /usr/bin/python3 -I -B tools/brain_check.py   # baseline šablony
# rc=0
brain-check: 2 stránek, 0 chyb, 0 varování

$ git switch -q -c brain/tester/pdf-export-limit
# rc=0
(bez výstupu)

$ /usr/bin/python3 -I -B tools/brain_check.py --write-index
# rc=0
brain-check: 3 stránek, 0 chyb, 0 varování

$ /usr/bin/python3 -I -B tools/brain_check.py   # s dobrou stránkou
# rc=0
brain-check: 3 stránek, 0 chyb, 0 varování

$ git -c user.name=Šablona test -c user.email=sablona-test@example.com add -A
# rc=0
(bez výstupu)

$ git -c user.name='Hermes (Testovací Člověk)' -c user.email=... commit -m '<zpráva>' --trailer 'Agent: …' --trailer 'Source: …' --trailer 'Co-authored-by: …'
# rc=0
(bez výstupu)

$ git log -1 --format=%B
# rc=0
kb(product): známá chyba – export PDF nad 500 položek

Agent: hermes/default@test-notebook
Source: example-org/fakturace#912
Co-authored-by: Testovací Člověk <tester@example.com>

$ /usr/bin/python3 -I -B tools/brain_check.py --commits main   # dobrý commit
# rc=0
brain-check: 3 stránek, 0 chyb, 0 varování

$ /usr/bin/python3 -I -B tools/brain_check.py   # špatné stránky (nepotvrzené rozhodnutí, bez zdroje, falešný token)
# rc=1
CHYBA: kb/decisions/dec-2026-0001.md: rozhodnutí čeká na potvrzení člověkem (status: proposed -> confirmed)
CHYBA: kb/product/bad-no-source.md: sources musí být neprázdný seznam s kind a ref
CHYBA: kb/product/bad-no-source.md: možné GitHub token: 'ghp_<36 znaků, zredigováno>'
brain-check: 5 stránek, 3 chyb, 0 varování

$ git switch -q main
# rc=0
(bez výstupu)

$ git switch -q -c brain/tester/bez-zdroje main
# rc=0
(bez výstupu)

$ git commit -am 'kb(glossary): zkouška' --trailer 'Agent: …'   # bez Source a Co-authored-by
# rc=0
(bez výstupu)

$ /usr/bin/python3 -I -B tools/brain_check.py --commits main   # commit bez traileru
# rc=1
CHYBA: commit 7c1ebb0: commit agenta bez traileru 'Source:'
CHYBA: commit 7c1ebb0: commit agenta bez traileru 'Co-authored-by:'
brain-check: 2 stránek, 2 chyb, 0 varování

$ git log --format=... main..HEAD
# rc=0
7c1ebb0 Hermes (Testovací Člověk) | hermes/default@test-notebook
 | kb(glossary): zkouška
```

Nebylo testováno: běh workflow `brain-check` na GitHubu, CODEOWNERS a ochrany větví (nastavení na GitHubu je v SETUP-GITHUB.md).
