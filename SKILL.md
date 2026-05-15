---
name: arch-flows-visualizer
description: "Generates interactive HTML visualizations of system architectures and flows from structured JSON data. Use when users request visual documentation of components, connections, data flows, processes, or system interactions in an engaging browser-based format. Trigger words include: visualize architecture, architecture flows diagram, interactive system map, create arch visualization, map components and flows, system architecture diagram."
---

# Arch Flows Visualizer

## Overview

This skill generates self-contained interactive single-page HTML visualizations for software systems and architectures. It displays components grouped into customizable columns, visual connections between them, selectable flows that highlight paths, and detailed step-by-step explanations.

## Instructions

- Determine whether the user's request would benefit from an interactive, browser-rendered architecture visualization rather than static text or simple diagrams.

- Construct or obtain a JSON data file that strictly follows the schema defined in `references/architecture-schema.json`. Use `references/example-data.json` as a concrete reference implementation (demonstrating a multi-column layout with actors, client surfaces, Firebase functions, storage, etc.).

- If the user supplies prose descriptions, existing diagrams, lists of services, or process narratives, systematically transform them into the required JSON structure:
  - Define `columns` with named groups and their `items` (each having id, label, optional sublabel, and type).
  - Populate `legend` for color/type coding.
  - Create `connections` with numbered links between item IDs.
  - Define `flows` as named sequences using connection numbers.
  - Provide `steps` with numbered explanations.

- Generate the visualization by invoking the bundled script:

  ```
  python /home/workdir/.grok/skills/arch-flows-visualizer/scripts/generate.py --data /path/to/your-architecture-data.json --output /home/workdir/artifacts
  ```

- The command produces:
  - `index.html` — fully interactive visualization (open in any modern browser).
  - `architecture-data.json` — copy of the source data for future edits.

- Key interactive features to highlight to users: clicking a flow highlights the corresponding path and components; clicking items reveals related connections; ESC key clears selections; responsive design suitable for presentations and documentation.

- For iteration: Edit the JSON source and re-execute the generation script. No server or build step is required.

- Prefer this skill for complex, multi-stage processes or architectures where flow selection and contextual step details add significant value. For simpler cases, consider whether built-in Mermaid or ASCII diagrams suffice.