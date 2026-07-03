#!/usr/bin/env python3
"""Assemble the generative-wrangler plugin from the repo's canonical sources.

The repo root holds the source of truth: `context/` (the library) and
`skills/*/SKILL.md` (the eleven skills, with bundled `references/`). This script
regenerates the plugin's single shared library and repoints every skill reference
at `${CLAUDE_PLUGIN_ROOT}/context/...` so there is no per-skill duplication.

Authored by hand (not touched here): plugin/.claude-plugin/plugin.json,
plugin/agents/*.md, plugin/README.md.

Usage:
    python plugin/assemble.py             # sync context/ + skills/, then validate
    python plugin/assemble.py --package   # also build the .plugin archive
"""
from __future__ import annotations
import argparse, json, re, shutil, sys, zipfile
from pathlib import Path

PLUGIN = Path(__file__).resolve().parent
REPO = PLUGIN.parent
CTX_SRC = REPO / "context"
SKILLS_SRC = REPO / "skills"
CTX_OUT = PLUGIN / "context"
SKILLS_OUT = PLUGIN / "skills"

SKILLS = ["project-context", "sequence-design", "shot-prompt", "model-docs", "footage-transform", "image-edit", "character-sheet", "prop-turntable", "location-pack", "art-direction", "production", "render", "dailies"]

HELPERS = [
    SKILLS_SRC / "project-context/references/questioning-framework.md",
    SKILLS_SRC / "project-context/references/output-template.md",
    SKILLS_SRC / "shot-prompt/references/model-layer-priority.md",
    SKILLS_SRC / "shot-prompt/references/output-examples.md",
    SKILLS_SRC / "model-docs/references/model-doc-template.md",
    SKILLS_SRC / "model-docs/references/example-model-doc.md",
    SKILLS_SRC / "character-sheet/references/character-template.md",
    SKILLS_SRC / "prop-turntable/references/prop-template.md",
    SKILLS_SRC / "location-pack/references/set-template.md",
    SKILLS_SRC / "art-direction/references/art-bible-template.md",
]

LINK_RE = re.compile(r"\]\(references/(?:models/)?([^)]*)\)")
ROOT = "${CLAUDE_PLUGIN_ROOT}/context/"
AGENT_REQUIRED = {"name", "description", "model", "color", "tools"}


def repoint(md):
    return LINK_RE.sub(lambda m: "](" + ROOT + m.group(1) + ")", md)


def sync_context():
    CTX_OUT.mkdir(parents=True, exist_ok=True)
    for f in sorted(CTX_SRC.glob("*.md")):
        shutil.copyfile(f, CTX_OUT / f.name)
    for h in HELPERS:
        if not h.exists():
            sys.exit("missing helper source: %s" % h)
        shutil.copyfile(h, CTX_OUT / h.name)
    print("context/: %d files" % len(list(CTX_OUT.glob("*.md"))))


def sync_skills():
    for name in SKILLS:
        src = SKILLS_SRC / name / "SKILL.md"
        out_dir = SKILLS_OUT / name
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "SKILL.md").write_text(repoint(src.read_text(encoding="utf-8")), encoding="utf-8")
        print("skill: %s" % name)


def validate():
    ok = True
    pj = PLUGIN / ".claude-plugin" / "plugin.json"
    try:
        meta = json.load(open(pj))
        assert re.fullmatch(r"[a-z0-9-]+", meta["name"]), "name not kebab-case"
    except Exception as e:
        print("FAIL plugin.json:", e); ok = False
    for name in SKILLS:
        sk = SKILLS_OUT / name / "SKILL.md"
        if not sk.exists():
            print("FAIL missing skill:", name); ok = False; continue
        body = sk.read_text(encoding="utf-8")
        for ref in re.findall(r"\]\((\$\{CLAUDE_PLUGIN_ROOT\}/[^)]+)\)", body):
            rel = ref.replace("${CLAUDE_PLUGIN_ROOT}/", "")
            if rel in ("context/", "context"):
                # bare shared-dir link can't resolve a specific doc (the uni-1 bug)
                print("FAIL %s: link to bare context/ dir — name the specific file: %s" % (name, ref)); ok = False
            elif rel.endswith("/"):
                if not (PLUGIN / rel).is_dir():
                    print("FAIL %s: link to missing dir %s" % (name, rel)); ok = False
            elif not (PLUGIN / rel).exists():
                print("FAIL %s: missing %s" % (name, rel)); ok = False
        if "](references/" in body:
            print("FAIL %s: stale references/ path remains" % name); ok = False
        # plugin loader caps the skill `description` frontmatter field at 1024 chars
        fm = re.match(r"---\s*\n(.*?)\n---", body, re.S)
        if fm:
            dm = re.search(r"^description:\s*(.*?)(?=\n[A-Za-z_-]+:\s|\Z)",
                           fm.group(1), re.S | re.M)
            if dm:
                val = dm.group(1).strip()
                if val[:1] in ">|":
                    val = val[1:]
                if val[:1] in "\"'" and val[-1:] in "\"'":
                    val = val[1:-1]
                dlen = len(re.sub(r"\s+", " ", val).strip())
                if dlen > 1024:
                    print("FAIL %s: description %d > 1024 chars" % (name, dlen)); ok = False
        # plugin loader rejects any XML/angle-bracket tag in SKILL.md (use {placeholder})
        tags = re.findall(r"<[^>\n]+>", body)
        if tags:
            print("FAIL %s: SKILL.md contains XML tags %s" % (name, tags[:3])); ok = False
    # agents: frontmatter must be strict-YAML-parseable (no raw <example> tags)
    # with the required keys. The plugin loader parses this as strict YAML.
    for a in sorted((PLUGIN / "agents").glob("*.md")):
        atext = a.read_text(encoding="utf-8")
        m = re.match(r"---\n(.*?)\n---\n", atext, re.S)
        if not m:
            print("FAIL agent (no frontmatter):", a.name); ok = False; continue
        atags = re.findall(r"<[^>\n]+>", atext[m.end():])
        if atags:
            print("FAIL %s: body contains XML tags %s" % (a.name, atags[:3])); ok = False
        keys = set()
        for line in m.group(1).splitlines():
            if not line.strip() or line[0] in " \t":
                continue
            if line.lstrip().startswith("<") or ":" not in line.split("#")[0]:
                print("FAIL %s: non-YAML frontmatter line: %r" % (a.name, line)); ok = False
            else:
                keys.add(line.split(":", 1)[0].strip())
        missing = AGENT_REQUIRED - keys
        if missing:
            print("FAIL %s: missing keys %s" % (a.name, sorted(missing))); ok = False
    print("VALIDATE: OK" if ok else "VALIDATE: ERRORS")
    return ok


def package():
    dest = REPO / "generative-wrangler.plugin"
    if dest.exists():
        dest.unlink()
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(PLUGIN.rglob("*")):
            if p.is_file() and p.name != "assemble.py" and not p.name.endswith(".plugin"):
                if any(part.startswith(".fuse_hidden") for part in p.parts):
                    continue
                z.write(p, p.relative_to(PLUGIN))
    print("packaged: %s (%d bytes)" % (dest, dest.stat().st_size))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--package", action="store_true")
    a = ap.parse_args()
    sync_context()
    sync_skills()
    ok = validate()
    if a.package and ok:
        package()
    sys.exit(0 if ok else 1)
