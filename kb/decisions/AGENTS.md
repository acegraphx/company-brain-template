# Pravidla pro návrhy rozhodnutí v kb/decisions/

Platí pro agenta, který pracuje s přepisem porady nebo hovoru. Doplňuje `AGENTS.md` v kořeni repa.

1. Jedno rozhodnutí = jeden soubor podle `templates/page-decision.md`.
2. Piš jen to, co na schůzce zaznělo jako rozhodnutí. Nápad, otázka, žert a odmítnutá varianta nejsou rozhodnutí.
3. Nový záznam má vždy `status: proposed`. Změnu na `confirmed` dělá účastník schůzky v PR, ne ty.
4. `meeting.transcript` je odkaz s časem (např. `meetings-raw:<id>#00:41:20`), nikdy text přepisu. Surový přepis do repa nekopíruj.
5. Odhadnutý vlastník, termín nebo účastník je návrh. V popisu PR ho označ jako návrh, nepiš ho jako fakt.
6. Položky `action_items` mají `what` a `who`. Z úkolů nic nezakládej jako issue; vzniknou až po sloučení.
7. Nové rozhodnutí nepřepisuje staré. Starý záznam dostane `status: superseded` a `superseded_by`, nový `supersedes`.
8. Nezapisuj osobní údaje, hodnocení lidí, HR témata ani citace účastníků.
9. Chybí-li zdroj nebo odkaz na přepis, záznam nenavrhuj. Zeptej se člověka.
