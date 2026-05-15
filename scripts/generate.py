#!/usr/bin/env python3
"""
Architecture Flows Visualizer Generator
Reads a JSON data file and produces a self-contained interactive single-page HTML
plus copies the JSON for editing.
"""

import argparse
import json
import os
import shutil
from datetime import datetime

def generate_html(data: dict) -> str:
    """Generate the full HTML content from architecture data."""
    
    # Prepare JSON for embedding (escaped properly)
    json_data = json.dumps(data, indent=2, ensure_ascii=False)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get("title", "Architecture & Flows")}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
        
        :root {{
            --bg-primary: #0f172a;
        }}
        
        body {{
            font-family: 'Inter', system_ui, sans-serif;
        }}
        
        .mono {{
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
        }}
        
        .architecture-container {{
            background: linear-gradient(145deg, #0f172a 0%, #1e293b 100%);
        }}
        
        .column-header {{
            background: #1e293b;
            border-bottom: 1px solid #334155;
            font-weight: 600;
            letter-spacing: 0.5px;
            font-size: 0.75rem;
            text-transform: uppercase;
        }}
        
        .arch-item {{
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid #475569;
        }}
        
        .arch-item:hover {{
            transform: translateY(-1px);
            box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.3);
        }}
        
        .arch-item.highlight {{
            border-color: #fbbf24 !important;
            box-shadow: 0 0 0 3px rgba(251, 191, 36, 0.3) !important;
            transform: scale(1.02);
            z-index: 10;
        }}
        
        .connection-number {{
            background: #334155;
            color: #e2e8f0;
            font-size: 0.65rem;
            width: 18px;
            height: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 9999px;
            font-weight: 700;
            box-shadow: 0 0 0 2px #1e293b;
        }}
        
        .flow-btn {{
            transition: all 0.15s ease;
        }}
        
        .flow-btn.active {{
            background-color: #334155;
            border-color: #64748b;
            box-shadow: 0 0 0 1px #64748b;
        }}
        
        .section-title {{
            font-size: 0.875rem;
            letter-spacing: 0.025em;
            font-weight: 600;
            color: #94a3b8;
        }}
        
        .diagram-grid {{
            scrollbar-width: thin;
            scrollbar-color: #475569 #1e293b;
        }}
        
        .path-step {{
            font-size: 0.75rem;
            padding: 2px 8px;
            background: #1e293b;
            border-radius: 4px;
        }}
        
        .legend-pill {{
            font-size: 0.65rem;
            padding: 1px 8px 1px 6px;
            border-radius: 9999px;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }}
    </style>
</head>
<body class="bg-slate-950 text-slate-200">
    <!-- Header -->
    <div class="border-b border-slate-800 bg-slate-900/80 backdrop-blur-lg sticky top-0 z-50">
        <div class="max-w-[1600px] mx-auto px-6 py-4 flex items-center justify-between">
            <div class="flex items-center gap-x-4">
                <div class="flex items-center gap-x-3">
                    <div class="w-9 h-9 bg-yellow-400 rounded-xl flex items-center justify-center shadow-inner">
                        <i class="fa-solid fa-project-diagram text-slate-950 text-2xl"></i>
                    </div>
                    <div>
                        <h1 class="text-2xl font-semibold tracking-tighter">{data.get("title", "Architecture & Flows")}</h1>
                        <p class="text-xs text-slate-400 -mt-0.5">System Architecture Visualization</p>
                    </div>
                </div>
            </div>
            
            <div class="flex items-center gap-x-3">
                <div class="px-3 py-1.5 bg-slate-900 border border-slate-700 rounded-2xl flex items-center text-xs">
                    <i class="fa-solid fa-info-circle mr-1.5 text-yellow-400"></i>
                    <span class="text-slate-400">Interactive — click flows to highlight paths</span>
                </div>
                
                <button onclick="downloadJSON()" 
                        class="flex items-center gap-x-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-600 text-xs rounded-2xl transition-colors">
                    <i class="fa-solid fa-download"></i>
                    <span>Download JSON</span>
                </button>
                
                <button onclick="window.location.reload()" 
                        class="px-3 py-2 text-xs flex items-center gap-x-1.5 bg-slate-800 hover:bg-slate-700 border border-slate-600 rounded-2xl transition-colors">
                    <i class="fa-solid fa-sync-alt"></i>
                </button>
            </div>
        </div>
    </div>

    <div class="max-w-[1600px] mx-auto px-6 pt-6 pb-12">
        
        <!-- Subtitle -->
        <div class="mb-6 max-w-3xl">
            <p class="text-slate-400 text-[15px] leading-relaxed">{data.get("subtitle", "")}</p>
        </div>
        
        <!-- Legend -->
        <div class="mb-8 flex flex-wrap items-center gap-2">
            <span class="text-xs uppercase tracking-[1px] text-slate-500 mr-3">LEGEND</span>
            {"".join([f'''<div class="legend-pill border border-slate-700 bg-slate-900 px-2.5 py-0.5"><span class="inline-block w-2 h-2 rounded-full {item["color"].replace("bg-", "bg-") if item["color"].startswith("bg-") else ""}" style="background-color: {item.get("color", "#64748b") if not item["color"].startswith("bg-") else ""}"></span><span class="text-xs text-slate-300">{item["label"]}</span></div>''' for item in data.get("legend", [])])}
        </div>
        
        <div class="flex gap-6">
            
            <!-- Main Diagram Area -->
            <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between mb-3 px-1">
                    <div class="section-title flex items-center gap-x-2">
                        <i class="fa-solid fa-sitemap"></i> 
                        <span>ARCHITECTURE COMPONENTS</span>
                    </div>
                    <div class="text-[10px] text-slate-500 mono">7 COLUMNS • {len(data.get("connections", []))} CONNECTIONS</div>
                </div>
                
                <!-- Columns Grid -->
                <div class="diagram-grid overflow-x-auto pb-4">
                    <div class="flex gap-3 min-w-max" id="columns-container">
                        <!-- Populated by JS -->
                    </div>
                </div>
                
                <!-- Connections Summary -->
                <div class="mt-4 bg-slate-900/70 border border-slate-800 rounded-3xl p-5">
                    <div class="flex items-center justify-between mb-4">
                        <div class="section-title flex items-center gap-x-2">
                            <i class="fa-solid fa-link"></i>
                            <span>KEY CONNECTIONS</span>
                        </div>
                        <span class="text-xs text-slate-500">Numbered paths used by flows</span>
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2 text-xs" id="connections-list">
                        <!-- Populated by JS -->
                    </div>
                </div>
            </div>
            
            <!-- Right Sidebar: Flows + Steps -->
            <div class="w-80 flex-shrink-0 space-y-6">
                
                <!-- Flows -->
                <div class="bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden">
                    <div class="px-5 pt-4 pb-3 border-b border-slate-800 flex items-center justify-between bg-slate-950/50">
                        <div class="section-title flex items-center gap-x-2">
                            <i class="fa-solid fa-route text-yellow-400"></i>
                            <span>FLOWS</span>
                        </div>
                        <button onclick="clearSelection()" 
                                class="text-[10px] px-2.5 py-px rounded-full bg-slate-800 text-slate-400 hover:text-slate-200 transition-colors">
                            CLEAR
                            </button>
                    </div>
                    
                    <div class="p-2 max-h-[380px] overflow-y-auto" id="flows-list">
                        <!-- Populated by JS -->
                    </div>
                </div>
                
                <!-- Steps -->
                <div class="bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden">
                    <div class="px-5 pt-4 pb-3 border-b border-slate-800 bg-slate-950/50">
                        <div class="section-title flex items-center gap-x-2">
                            <i class="fa-solid fa-list-ol text-emerald-400"></i>
                            <span>STEPS</span>
                        </div>
                    </div>
                    
                    <div class="p-4 space-y-4 max-h-[280px] overflow-y-auto" id="steps-list">
                        <!-- Populated by JS -->
                    </div>
                </div>
                
            </div>
            
        </div>
        
        <!-- Footer note -->
        <div class="mt-8 text-center">
            <p class="text-[10px] text-slate-500">Generated on {datetime.now().strftime("%B %d, %Y at %H:%M")} • Edit the accompanying JSON file and re-run the generator to update</p>
        </div>
        
    </div>
    
    <script>
        // Embedded Architecture Data
        const architectureData = {json_data};
        
        let currentHighlightedFlow = null;
        
        function renderColumns() {{
            const container = document.getElementById('columns-container');
            container.innerHTML = '';
            
            const typeColorMap = {{}};
            architectureData.legend.forEach(l => {{
                typeColorMap[l.type] = l.color;
            }});
            
            architectureData.columns.forEach(column => {{
                const colDiv = document.createElement('div');
                colDiv.className = 'w-44 flex-shrink-0 bg-slate-900 border border-slate-700 rounded-3xl overflow-hidden shadow-xl';
                
                // Header
                const header = document.createElement('div');
                header.className = 'column-header px-3.5 py-2.5 text-center text-slate-300';
                header.innerHTML = `<span class="font-mono tracking-[1.5px]">${{column.name}}</span>`;
                colDiv.appendChild(header);
                
                // Items
                const itemsContainer = document.createElement('div');
                itemsContainer.className = 'p-2 space-y-1.5 bg-slate-950/50';
                
                column.items.forEach(item => {{
                    const itemEl = document.createElement('div');
                    itemEl.className = `arch-item px-3 py-2.5 rounded-2xl bg-slate-900 cursor-pointer text-sm`;
                    itemEl.setAttribute('data-id', item.id);
                    
                    const colorClass = typeColorMap[item.type] || 'bg-slate-600';
                    
                    let html = `
                        <div class="flex items-start gap-x-2.5">
                            <div class="mt-0.5 flex-shrink-0">
                                <span class="inline-block w-2.5 h-2.5 rounded-full ${{colorClass}} ring-1 ring-offset-2 ring-offset-slate-900 ring-slate-700"></span>
                            </div>
                            <div class="min-w-0 flex-1">
                                <div class="font-medium text-slate-100 leading-tight">${{item.label}}</div>
                    `;
                    
                    if (item.sublabel) {{
                        html += `<div class="text-[10px] text-slate-400 leading-none mt-0.5 mono">${{item.sublabel}}</div>`;
                    }}
                    
                    html += `</div></div>`;
                    itemEl.innerHTML = html;
                    
                    // Click to highlight related
                    itemEl.onclick = () => highlightRelatedComponents(item.id);
                    
                    itemsContainer.appendChild(itemEl);
                }});
                
                colDiv.appendChild(itemsContainer);
                container.appendChild(colDiv);
            }});
        }}
        
        function renderConnections() {{
            const container = document.getElementById('connections-list');
            container.innerHTML = '';
            
            if (!architectureData.connections || architectureData.connections.length === 0) {{
                container.innerHTML = '<div class="col-span-3 text-center py-4 text-xs text-slate-500">No connections defined</div>';
                return;
            }}
            
            architectureData.connections.forEach(conn => {{
                const div = document.createElement('div');
                div.className = 'flex items-center gap-x-2 text-xs px-3 py-2 bg-slate-950 border border-slate-800 rounded-2xl hover:border-slate-700 transition-colors';
                
                const fromItem = findItemById(conn.from);
                const toItem = findItemById(conn.to);
                
                div.innerHTML = `
                    <div class="flex-shrink-0">
                        <span class="connection-number font-mono">${{conn.number}}</span>
                    </div>
                    <div class="flex-1 min-w-0 text-[11px] leading-tight">
                        <span class="font-medium text-slate-300">${{fromItem ? fromItem.label : conn.from}}</span>
                        <span class="mx-1 text-slate-500">→</span>
                        <span class="font-medium text-slate-300">${{toItem ? toItem.label : conn.to}}</span>
                    </div>
                `;
                
                container.appendChild(div);
            }});
        }}
        
        function findItemById(id) {{
            for (const col of architectureData.columns) {{
                const found = col.items.find(i => i.id === id);
                if (found) return found;
            }}
            return null;
        }}
        
        function renderFlows() {{
            const container = document.getElementById('flows-list');
            container.innerHTML = '';
            
            if (!architectureData.flows || architectureData.flows.length === 0) {{
                container.innerHTML = '<div class="px-4 py-6 text-center text-xs text-slate-500">No flows defined</div>';
                return;
            }}
            
            architectureData.flows.forEach(flow => {{
                const btn = document.createElement('button');
                btn.className = `flow-btn w-full text-left px-4 py-3 mb-1.5 rounded-2xl border border-transparent hover:border-slate-700 flex items-start gap-x-3 group`;
                btn.setAttribute('data-flow-id', flow.id);
                
                btn.innerHTML = `
                    <div class="pt-0.5">
                        <i class="fa-solid fa-play text-yellow-400 group-hover:text-yellow-300 transition-colors text-xs"></i>
                    </div>
                    <div class="flex-1 min-w-0">
                        <div class="font-semibold text-sm text-slate-100 leading-tight pr-1">${{flow.name}}</div>
                        <div class="text-[10px] text-slate-400 line-clamp-2 mt-0.5">${{flow.description}}</div>
                        
                        <div class="mt-2 flex flex-wrap gap-1">
                            ${{flow.path.map(n => `<span class="inline-block text-[9px] px-1.5 py-px bg-slate-800 text-yellow-300/80 rounded font-mono">${{n}}</span>`).join('')}} 
                        </div>
                    </div>
                `;
                
                btn.onclick = () => selectFlow(flow, btn);
                
                container.appendChild(btn);
            }});
        }}
        
        function renderSteps() {{
            const container = document.getElementById('steps-list');
            container.innerHTML = '';
            
            if (!architectureData.steps || architectureData.steps.length === 0) {{
                container.innerHTML = '<div class="text-xs text-slate-500 px-1">No steps defined</div>';
                return;
            }}
            
            architectureData.steps.forEach(step => {{
                const div = document.createElement('div');
                div.className = 'flex gap-3';
                
                div.innerHTML = `
                    <div class="flex-shrink-0 w-6 h-6 mt-0.5 rounded-full bg-emerald-900/70 flex items-center justify-center text-emerald-300 text-xs font-bold border border-emerald-700">
                        ${{step.number}}
                    </div>
                    <div class="flex-1 min-w-0">
                        <div class="font-semibold text-sm text-emerald-100">${{step.title}}</div>
                        <div class="text-xs text-slate-400 whitespace-pre-line mt-0.5 leading-snug">${{step.description}}</div>
                    </div>
                `;
                
                container.appendChild(div);
            }});
        }}
        
        function selectFlow(flow, btnElement) {{
            // Clear previous
            clearSelection(false);
            
            // Activate button
            btnElement.classList.add('active', 'border-yellow-400/60', 'bg-slate-800');
            currentHighlightedFlow = flow.id;
            
            // Highlight path
            highlightPath(flow.path);
            
            // Scroll to top of diagram
            document.querySelector('.diagram-grid').scrollIntoView({{ behavior: 'smooth', block: 'center' }});
        }}
        
        function highlightPath(pathNumbers) {{
            // Find all involved component IDs from the path connections
            const involvedIds = new Set();
            
            pathNumbers.forEach(num => {{
                const conn = architectureData.connections.find(c => c.number === num);
                if (conn) {{
                    involvedIds.add(conn.from);
                    involvedIds.add(conn.to);
                }}
            }});
            
            // Add highlight class to matching elements
            document.querySelectorAll('.arch-item').forEach(el => {{
                const itemId = el.getAttribute('data-id');
                if (involvedIds.has(itemId)) {{
                    el.classList.add('highlight');
                }}
            }});
            
            // Optional: show toast with path info
            showPathToast(pathNumbers);
        }}
        
        function showPathToast(pathNumbers) {{
            const existing = document.getElementById('path-toast');
            if (existing) existing.remove();
            
            const toast = document.createElement('div');
            toast.id = 'path-toast';
            toast.className = 'fixed bottom-6 left-1/2 -translate-x/2 bg-slate-900 border border-yellow-400/30 text-yellow-100 px-6 py-3 rounded-3xl shadow-2xl flex items-center gap-x-3 text-sm z-[100]';
            
            const pathHTML = pathNumbers.map(n => `<span class="px-2 py-0.5 bg-yellow-400/10 text-yellow-300 rounded-xl font-mono text-xs">${{n}}</span>`).join('');
            
            toast.innerHTML = `
                <div class="flex items-center gap-x-2">
                    <i class="fa-solid fa-link text-yellow-400"></i>
                    <span class="font-medium">Path highlighted:</span> 
                    <span class="flex gap-1">${{pathHTML}}</span>
                </div>
            `;
            
            document.body.appendChild(toast);
            
            setTimeout(() => {{
                if (toast && toast.parentNode) toast.parentNode.removeChild(toast);
            }}, 3800);
        }}
        
        function highlightRelatedComponents(itemId) {{
            clearSelection(false);
            
            // Find connections involving this item
            const relatedConns = architectureData.connections.filter(c => c.from === itemId || c.to === itemId);
            const relatedNumbers = relatedConns.map(c => c.number);
            
            // Highlight the item itself
            document.querySelectorAll(`.arch-item[data-id="${{itemId}}"]`).forEach(el => {{
                el.classList.add('highlight');
            }});
            
            // Highlight connected items
            const connectedIds = new Set();
            relatedConns.forEach(c => {{
                connectedIds.add(c.from);
                connectedIds.add(c.to);
            }});
            
            connectedIds.forEach(id => {{
                document.querySelectorAll(`.arch-item[data-id="${{id}}"]`).forEach(el => {{
                    if (el.getAttribute('data-id') !== itemId) {{
                        el.classList.add('highlight');
                    }}
                }});
            }});
            
            // Show related connections in console or toast
            if (relatedNumbers.length > 0) {{
                const toast = document.createElement('div');
                toast.className = 'fixed bottom-6 right-6 bg-slate-900 border border-slate-700 px-4 py-2 rounded-2xl text-xs shadow-xl z-[100]';
                toast.innerHTML = `Connected via steps: <span class="font-mono text-yellow-300">${{relatedNumbers.join(', ')}}</span>`;
                document.body.appendChild(toast);
                setTimeout(() => toast.remove(), 2200);
            }}
        }}
        
        function clearSelection(resetFlow = true) {{
            // Remove all highlights
            document.querySelectorAll('.arch-item').forEach(el => {{
                el.classList.remove('highlight');
            }});
            
            // Deactivate flow buttons
            document.querySelectorAll('.flow-btn').forEach(btn => {{
                btn.classList.remove('active', 'border-yellow-400/60', 'bg-slate-800');
            }});
            
            // Remove any toasts
            const toast = document.getElementById('path-toast');
            if (toast) toast.remove();
            
            if (resetFlow) {{
                currentHighlightedFlow = null;
            }}
        }}
        
        function downloadJSON() {{
            const dataStr = JSON.stringify(architectureData, null, 2);
            const blob = new Blob([dataStr], {{ type: 'application/json' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'architecture-data.json';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }}
        
        function initialize() {{
            // Render all sections
            renderColumns();
            renderConnections();
            renderFlows();
            renderSteps();
            
            // Keyboard support: ESC clears
            document.addEventListener('keydown', function(e) {{
                if (e.key === 'Escape') {{
                    clearSelection();
                }}
            }});
            
            // Demo: Auto-highlight first flow after 1.2s if present (optional, comment out for production)
            // setTimeout(() => {{
            //     const firstFlowBtn = document.querySelector('.flow-btn');
            //     if (firstFlowBtn && architectureData.flows.length > 0) {{
            //         firstFlowBtn.click();
            //     }}
            // }}, 1200);
            
            console.log('%c[Arch Visualizer] Interactive diagram initialized successfully', 'color:#64748b');
        }}
        
        // Boot
        window.onload = initialize;
    </script>
</body>
</html>'''
    
    return html

def main():
    parser = argparse.ArgumentParser(description="Generate Architecture Flows HTML + JSON")
    parser.add_argument('--data', '-d', required=True, help='Path to input JSON data file')
    parser.add_argument('--output', '-o', default='/home/workdir/artifacts', help='Output directory')
    args = parser.parse_args()
    
    # Load data
    with open(args.data, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Generate HTML
    html_content = generate_html(data)
    
    # Ensure output dir
    os.makedirs(args.output, exist_ok=True)
    
    # Write HTML
    html_path = os.path.join(args.output, 'index.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Copy JSON for reference/editing
    json_path = os.path.join(args.output, 'architecture-data.json')
    shutil.copy2(args.data, json_path)
    
    print(f"✅ Successfully generated:")
    print(f"   • {html_path}")
    print(f"   • {json_path}")
    print(f"\nOpen {html_path} in a browser to view the interactive diagram.")

if __name__ == "__main__":
    main()