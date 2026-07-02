# {SHOW} - Art Bible

> Template — replace every `{token}` with real values; delete this line when the bible is complete.

## Inherits

- Project context: [`{show}_project_context.md`]({show}_project_context.md)
- Inherited lens: {lens spec from project-context, e.g. 35mm, T2.8}
- Inherited grade: {grade description from project-context, e.g. teal-orange, crushed blacks}
- Standard Prompt Prefix: *(paste verbatim from {show}_project_context.md)*

---

## Global palette

| Role     | Name         | Hex     | Finish notes              |
|----------|--------------|---------|---------------------------|
| Dominant | {color-name} | #{hex}  | matte / satin / gloss     |
| Dominant | {color-name} | #{hex}  | {finish}                  |
| Accent   | {color-name} | #{hex}  | {finish}                  |
| Accent   | {color-name} | #{hex}  | {finish}                  |
| Skin ref | {color-name} | #{hex}  | subsurface, not a surface |

Every surface description in an asset prompt uses the form `{name}, {hex}, {finish}`.
Restate the relevant palette entries in each asset's identity block — do not rely on agents
reading the bible for every generation.

---

## CMF lexicon

Material/finish/texture terms shared across every asset in this world. Copy entries verbatim
into asset prompts; do not rephrase.

```
{short-name}:   {material call}, {finish call}, {texture note}
{short-name}:   {material call}, {finish call}, {texture note}
{short-name}:   {material call}, {finish call}, {texture note}
```

Examples of well-formed entries:
```
aged-brass:     cast brass, verdigris patina, slight surface relief at seams
raw-concrete:   poured concrete, unsealed, fine aggregate visible, hairline cracks at joints
worn-linen:     natural linen, preshrunk, pulled threads at collar and cuffs
```

To add a new material to the world, define it here first, then use it in the asset sheet.

---

## Era / genre / world rules

World prompt prefix (prepend to first-generation asset prompts):
`World: {era}, {genre register}, {technology level}, {entropy level}.`

Hard constraints — every generated asset must pass this checklist:

- **Period:** {e.g. 1930s rural American South / near-future 2040s / mythic undated}
- **Genre register:** {e.g. social realist / neo-noir / magical realist}
- **Technology level:** {e.g. pre-electrification / analogue industrial / post-digital}
- **Entropy level:** {pristine / lived-in / decayed / ruined} — apply globally; override per
  asset only with explicit justification documented in that asset's spec file
- **Forbidden materials / forms:** {e.g. no chrome, no plastics, no synthetic textiles}
- **Additional world constraints:** {list any genre departures or world-specific rules
  explicitly — agents default to genre convention if the exception is not named here}

---

## Global style reference

Path: `assets/style/style-{show}_global.png`

This image anchors the visual register of the world — light quality, surface feel, color
temperature, tonal contrast. Attach it as a background reference to every first-generation
asset prompt. It is not a composition reference and does not substitute for palette hex
values, CMF entries, or era/genre rules.

Generated via `image-edit` from mood-board inputs guided by the palette, CMF lexicon, and
era/genre rules above. Lock date: {YYYY-MM-DD}. Supersedes any prior draft.

---

## Asset index

Populate as assets are locked — spec-filed and anchor-imaged. Do not list unlocked assets.
Update this table when an anchor image is replaced or an asset is retired.

Spec-file names carry `{show}`; image-file names do not.

| Type   | Name     | Spec file               | Anchor image path                             |
|--------|----------|-------------------------|-----------------------------------------------|
| `char` | `{name}` | `{show}_char_{name}.md` | `assets/char/{name}/{show}_char_{name}_id_front.png` |
| `prop` | `{name}` | `{show}_prop_{name}.md` | `assets/prop/{name}/{show}_prop_{name}_hero.png`     |
| `set`  | `{name}` | `{show}_set_{name}.md`  | `assets/set/{name}/{show}_set_{name}_plate.png`      |

*(Add rows as assets are locked. Remove the example rows above when populating with real assets.)*
