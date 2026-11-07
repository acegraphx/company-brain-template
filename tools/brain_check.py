#!/usr/bin/env python3
"""brain-check: kontrola stránek company-brain (náčrt pro workshop, stdlib + PyYAML)."""
import argparse, datetime as dt, pathlib, re, subprocess, sys
try:
    import yaml
except ImportError:
    sys.exit("Chybí PyYAML: pip install pyyaml")

ROOT = pathlib.Path(__file__).resolve().parent.parent
REQUIRED = ["id", "title", "type", "status", "owner", "sensitivity", "sources",
            "confidence", "created", "updated", "review_by"]
ENUMS = {"type": {"concept", "decision", "runbook", "known-issue", "faq", "glossary"},
         "sensitivity": {"internal"},
         "confidence": {"high", "medium", "low"}}
STATUS = {"decision": {"proposed", "confirmed", "superseded"}}   # ostatní typy: official | deprecated
DECISION_FIELDS = ["decision", "decided_by", "decided_on", "participants", "meeting"]
SKIP = {"AGENTS.md", "README.md"}
PATTERNS = {
    "e-mail": r"[\w.+-]+@[\w-]+\.[\w.-]+",
    "telefon": r"(?<![\w/#-])(?:\+420 ?)?\d{3} ?\d{3} ?\d{3}(?![\w-])",
    "privátní klíč": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "GitHub token": r"\b(?:ghp|gho|ghs|ghu|github_pat)_[A-Za-z0-9_]{20,}",
    "API klíč": r"\b(?:sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|xox[abpr]-[A-Za-z0-9-]{10,})",
    "instrukce pro model": r"(?i)(?:ignore|disregard) (?:all |any )?(?:previous|prior|above) instructions"
                           r"|system prompt|ignoruj (?:všechny |předchozí )+instrukce",
    "skrytý HTML komentář": r"<!--",
}
ALLOW = {"git@github.com"}

def pages():
    for p in sorted((ROOT / "kb").rglob("*.md")):
        if p.name not in SKIP:
            yield p

def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    return yaml.safe_load(text[4:end]) if end > 0 else None

def owners():
    f = ROOT / ".github" / "CODEOWNERS"
    return set(re.findall(r"@[\w.-]+/[\w.-]+|@[\w.-]+", f.read_text())) if f.exists() else set()

def build_index(meta):
    rows = ["# Index (generováno: python3 tools/brain_check.py --write-index)", "",
            "| id | název | typ | vlastník | přezkoumat do | soubor |", "|---|---|---|---|---|---|"]
    for path, fm in sorted(meta.items()):
        rows.append(f"| {fm['id']} | {fm['title']} | {fm['type']} | {fm['owner']} | {fm['review_by']} | [{path}]({path}) |")
    return "\n".join(rows) + "\n"

def check_commits(base):
    out = subprocess.run(["git", "log", "--format=%H%x00%B%x1e", f"{base}..HEAD"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    errs = []
    for chunk in filter(None, (c.strip() for c in out.split("\x1e"))):
        sha, _, body = chunk.partition("\x00")
        if re.search(r"^Agent: ", body, re.M):
            for t in ("Source: ", "Co-authored-by: "):
                if not re.search(rf"^{t}", body, re.M):
                    errs.append(f"commit {sha[:7]}: commit agenta bez traileru '{t.strip()}'")
    return errs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-index", action="store_true")
    ap.add_argument("--commits", metavar="BASE", help="zkontrolovat trailery commitů BASE..HEAD")
    a = ap.parse_args()
    errs, warns, meta, ids = [], [], {}, {}
    known_owners, today = owners(), dt.date.today()
    for p in pages():
        rel, text = p.relative_to(ROOT).as_posix(), p.read_text(encoding="utf-8")
        fm = frontmatter(text)
        if not isinstance(fm, dict):
            errs.append(f"{rel}: chybí frontmatter"); continue
        miss = [k for k in REQUIRED if k not in fm]
        if miss:
            errs.append(f"{rel}: chybí pole {', '.join(miss)}"); continue
        for k, allowed in ENUMS.items():
            if fm[k] not in allowed:
                errs.append(f"{rel}: {k}={fm[k]!r} není v {sorted(allowed)}")
        allowed = STATUS.get(fm["type"], {"official", "deprecated"})
        if fm["status"] not in allowed:
            errs.append(f"{rel}: status={fm['status']!r} není v {sorted(allowed)}")
        if fm["type"] == "decision":
            miss = [k for k in DECISION_FIELDS if k not in fm]
            if miss:
                errs.append(f"{rel}: rozhodnutí bez polí {', '.join(miss)}")
            elif not (isinstance(fm["meeting"], dict) and fm["meeting"].get("date") and fm["meeting"].get("transcript")):
                errs.append(f"{rel}: meeting musí mít date a transcript (odkaz s časem, ne text)")
            if fm["status"] == "proposed":
                errs.append(f"{rel}: rozhodnutí čeká na potvrzení člověkem (status: proposed -> confirmed)")
            if fm["status"] == "superseded" and not fm.get("superseded_by"):
                errs.append(f"{rel}: superseded bez superseded_by")
            for it in fm.get("action_items") or []:
                if not (isinstance(it, dict) and it.get("what") and it.get("who")):
                    errs.append(f"{rel}: úkol v action_items musí mít what a who")
        if fm["id"] in ids:
            errs.append(f"{rel}: id {fm['id']} už má {ids[fm['id']]}")
        ids[fm["id"]] = rel
        if fm["owner"] not in known_owners:
            errs.append(f"{rel}: vlastník {fm['owner']} není v CODEOWNERS")
        src = fm["sources"]
        if not isinstance(src, list) or not src or not all(isinstance(s, dict) and s.get("kind") and s.get("ref") for s in src):
            errs.append(f"{rel}: sources musí být neprázdný seznam s kind a ref")
        else:
            for s in src:
                if s["kind"] == "customer-report" and s.get("trust") != "untrusted":
                    errs.append(f"{rel}: zdroj {s['ref']} od zákazníka musí mít trust: untrusted")
            if all(s.get("trust") == "untrusted" for s in src) and fm["confidence"] == "high":
                errs.append(f"{rel}: jen z nedůvěryhodných zdrojů nemůže být confidence: high")
        for k in ("created", "updated", "review_by"):
            if not isinstance(fm[k], dt.date):
                errs.append(f"{rel}: {k} není datum RRRR-MM-DD")
        if isinstance(fm["review_by"], dt.date) and fm["review_by"] < today:
            warns.append(f"{rel}: review_by {fm['review_by']} vypršelo, upozornit vlastníka {fm['owner']}")
        for label, rx in PATTERNS.items():
            for m in re.finditer(rx, text):
                if m.group(0) not in ALLOW:
                    errs.append(f"{rel}: možné {label}: {m.group(0)[:40]!r}")
        meta[rel] = fm
    index = ROOT / "index.md"
    if not errs:
        new = build_index(meta)
        if a.write_index:
            index.write_text(new, encoding="utf-8")
        elif not index.exists() or index.read_text(encoding="utf-8") != new:
            errs.append("index.md neodpovídá stránkám: spusť python3 tools/brain_check.py --write-index")
    if a.commits:
        errs += check_commits(a.commits)
    for w in warns:
        print("VAROVÁNÍ:", w)
    for e in errs:
        print("CHYBA:", e)
    print(f"brain-check: {len(meta)} stránek, {len(errs)} chyb, {len(warns)} varování")
    return 1 if errs else 0

if __name__ == "__main__":
    sys.exit(main())
