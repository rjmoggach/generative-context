# {SHOW} - {Name} - Location/Set Pack

---

## Master plate

- **Plate:** `assets/set/{name}/set-{name}-plate.png`
- **Geometry notes:** {primary sight line, horizon position, key architectural anchors,
  background depth — e.g., "long axis left-to-right; window at screen-right is the only
  practical source; brick end wall at frame-left closes depth"}
- **Light logic:** {dominant source, key direction, colour temp with hex, time of day at
  base state — e.g., "overhead south key, hard, neutral `#FFF5E4`, late-morning base"}

Example (show: sbw, name: livingroom):
- `assets/set/livingroom/set-livingroom-plate.png`

> **Identity block** — paste verbatim into every downstream shot prompt:
>
> {50–80 words. Environment class, era, primary materials and finishes with hex,
> dominant spatial axes and key sight line, practical light sources and their positions,
> critical atmospheric or grade note. Hex-pinned. Example: "1940s warehouse interior,
> raw concrete walls (`#4A4A42`), timber floor (`#7B5C3A`), single clerestory window on
> the north wall admitting a hard afternoon key, exposed iron columns, receding depth
> along the west wall, no soft fill — hard shadow rake dominant."}

---

## Coverage

### Coverage 01

- **Image:** `assets/set/{name}/set-{name}-cov-01.png`
- **Angle:** {description — e.g., "tight on the window wall from inside, looking south"}
- **Derived from:** master plate
- **Landmarks:** {architectural feature held consistent with master — e.g., "north column
  visible at frame-left"}

Example (name: livingroom):
- `assets/set/livingroom/set-livingroom-cov-01.png`

### Reverse angle

- **Image:** `assets/set/{name}/set-{name}-cov-reverse.png`
- **Angle:** reverse — looking back along the master plate's primary sight line
- **Derived from:** master plate
- **Landmarks:** {landmarks shared with master plate that confirm geometry is consistent —
  e.g., "doorway arch from master now at frame-right; floor seam continues; window
  light entering from same source, now at screen-left"}

Example (name: livingroom):
- `assets/set/livingroom/set-livingroom-cov-reverse.png`

### Coverage 02 *(add a section for each additional angle)*

- **Image:** `assets/set/{name}/set-{name}-cov-02.png`
- **Angle:** {description}
- **Derived from:** {source — usually master plate}
- **Landmarks:** {shared continuity anchors}

---

## Time-of-day / weather variants

*Each variant changes exactly one variable from the master plate or the nearest prior
variant. State the single changed axis and the resulting light, colour, and atmosphere.*

### Base (day)

- **Image:** `assets/set/{name}/set-{name}-plate.png` *(the master plate; no change)*
- **Variable changed:** — *(baseline)*
- **Light direction:** {e.g., overhead south, hard}
- **Colour:** neutral `#FFF5E4`
- **Atmosphere:** clear

### Dawn

- **Image:** `assets/set/{name}/set-{name}-tod-dawn.png`
- **Variable changed:** time of day (dawn)
- **Light direction:** {low east, soft}
- **Colour:** cool `#B8D4E8`
- **Atmosphere:** {e.g., light mist, softened contrast}

Example (name: livingroom):
- `assets/set/livingroom/set-livingroom-tod-dawn.png`

### Golden hour

- **Image:** `assets/set/{name}/set-{name}-tod-golden.png`
- **Variable changed:** time of day (late afternoon)
- **Light direction:** {low west, hard, long raking shadows}
- **Colour:** warm amber `#FFB347`
- **Atmosphere:** {e.g., clear, long shadows raking through the space}

### Night

- **Image:** `assets/set/{name}/set-{name}-tod-night.png`
- **Variable changed:** time of day (night)
- **Light direction:** {overhead minimal ambient, practical-dominant}
- **Colour:** cool blue-black `#1A1F2E`
- **Atmosphere:** {e.g., deep shadow, practicals as primary key}

### Rain / overcast *(add a section for each additional variant)*

- **Image:** `assets/set/{name}/set-{name}-tod-rain.png`
- **Variable changed:** weather (rain added to base)
- **Light direction:** {top, diffuse}
- **Colour:** grey-green `#B8C4B0`
- **Atmosphere:** {e.g., rain haze, wet surfaces, desaturated palette}

---

## Continuity table

*Restate this table verbatim in every shot prompt that places action in this location.*

| Variant | Key direction | Colour | Atmosphere |
|---------|--------------|--------|------------|
| Base (day) | {e.g., overhead south, hard} | neutral `#FFF5E4` | clear |
| Dawn | {low east, soft} | cool `#B8D4E8` | light mist |
| Golden | {low west, hard} | warm amber `#FFB347` | long shadows |
| Night | {practical-key, overhead ambient} | cool `#1A1F2E` | deep shadow |
| Rain | {top, diffuse} | grey-green `#B8C4B0` | rain haze, wet surfaces |

*Add or trim rows to match the variants actually generated. Hex-pin every Colour entry.*

---

## Reference notes

- **Reference images total:** {N}
- **Reference strength:** {0.0–1.0} (range across sessions: {min}–{max})
- **Model:** {name and version — e.g., FLUX.1 Kontext, 2026-06}
- **Currency check:** {date verified against model-currency-{month}.md}
- **Notes:** {known drift points, model weaknesses, watch items — e.g., background sky
  varies in wides; lock horizon line; reflective surfaces blow out above strength 0.75}
