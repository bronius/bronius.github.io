Self-hosted, subset WOFF2 (Latin + typographic punctuation). Both families are SIL Open Font License 1.1.

- `rye.woff2`: Rye by Nicole Fally (Sorkin Type). License: `OFL-Rye.txt`.
- `lora-{400,600,400i}.woff2`: Lora by Cyreal, static instances cut from the variable font.

Rebuild: `pyftsubset` (fontTools) with `--flavor=woff2`; see redesign/STATUS.md for the unicode ranges.
