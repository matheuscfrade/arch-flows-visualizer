# Arch Flows Visualizer

**Interactive HTML visualizations for system architectures and flows from structured JSON data.**

This repository packages the `arch-flows-visualizer` skill originally built for Grok (by xAI). It enables the creation of beautiful, self-contained, browser-based diagrams that show components, connections, selectable flows, and detailed process steps.

## ✨ Features

- **Self-contained single-file HTML** — No build step or external dependencies at runtime (uses Tailwind via CDN + Font Awesome)
- **Multi-column layout** for organizing components (e.g., Actors, Services, Storage, Pipelines)
- **Numbered connections** between components
- **Interactive flows** — Click any flow on the sidebar to highlight the exact path through the architecture
- **Component highlighting** — Click items to see related connections
- **Step-by-step explanations** panel
- **Keyboard support** (ESC to clear selections)
- **Responsive** and presentation-ready
- **JSON-driven** — Easy to version, edit, and regenerate

## 📁 Repository Structure

```
arch-flows-visualizer/
├── README.md
├── SKILL.md                 # Instructions for using as a Grok/xAI skill
├── scripts/
│   └── generate.py          # Python generator (produces index.html + architecture-data.json)
└── references/
    ├── architecture-schema.json
    └── example-data.json    # Full example (ToDesktop architecture)
```

## 🚀 Quick Start (Standalone)

1. **Clone the repository**
   ```bash
   git clone https://github.com/matheuscfrade/arch-flows-visualizer.git
   cd arch-flows-visualizer
   ```

2. **Prepare your data**
   - Follow the schema in `references/architecture-schema.json`
   - Use `references/example-data.json` as a reference

3. **Generate the visualization**
   ```bash
   python scripts/generate.py --data references/example-data.json --output ./dist
   ```

4. **View it**
   Open `dist/index.html` in any modern browser.

## 🛠️ Using as a Grok Skill

See [SKILL.md](./SKILL.md) for detailed instructions on how this skill is invoked by Grok, including how to transform user descriptions into the required JSON format and run the generator.

## 🔄 Iteration Workflow

1. Edit your `your-architecture.json`
2. Re-run the generator script
3. Refresh the browser

No servers, no bundlers, no friction.

## 📄 License

This project is provided as-is for use with Grok and general architecture documentation purposes.

---

**Originally developed as a Grok skill.**  
Repository maintained by Matheus Frade.