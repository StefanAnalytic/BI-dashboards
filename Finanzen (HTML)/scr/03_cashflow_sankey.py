# ==============================================================================
# DATEINAME: 03_cashflow_sankey.py
# VIEW: 03 - Dynamic Cashflow Sankey & Value Stream Analysis
# ==============================================================================
"""
Dieses Skript generiert die dritte Ansichtsseite (View 03).
Es beinhaltet ein interaktives, mathematisch präzises Sankey-Diagramm (SVG),
das den Kapitalfluss (Revenue -> COGS -> OPEX -> Net Income) darstellt.
Die Pfeiltasten LINKS/RECHTS navigieren durch die Wertschöpfungsstufen.
Dabei werden Predictive Variances (Abweichungen vom ML-Forecast) dynamisch eingeblendet.
"""

import json

class CashflowSankeyBuilder:
    def __init__(self):
        self.view_id = "view-03"
        
        # High-End Data Payload für die Sankey-Stufen
        self.flow_stages = [
            {
                "stage": "Revenue",
                "id": "node-rev",
                "value": "€240.5M",
                "variance": "+4.2%",
                "ds_insight": "ARIMA Model: Top-line outperforming baseline due to Q3 seasonal anomaly."
            },
            {
                "stage": "Gross Margin",
                "id": "node-gm",
                "value": "€168.3M",
                "variance": "-1.1%",
                "ds_insight": "COGS Spike detected. Isolation Forest flags supplier index variance."
            },
            {
                "stage": "EBITDA",
                "id": "node-ebitda",
                "value": "€95.2M",
                "variance": "+2.8%",
                "ds_insight": "OPEX efficiency high. Marketing ROI clusters show optimized CPA."
            },
            {
                "stage": "Net Income",
                "id": "node-ni",
                "value": "€64.8M",
                "variance": "+5.1%",
                "ds_insight": "Tax optimization algorithm yielded lower effective tax rate."
            }
        ]

    def build_css(self) -> str:
        """CSS für das Sankey-Diagramm, Flow-Animationen und Data-Panels."""
        return """
        /* ==========================================================================
           VIEW 03: SANKEY DIAGRAM STYLES
           ========================================================================== */
        #view-03 {
            display: grid;
            grid-template-columns: 1fr;
            grid-template-rows: auto 1fr;
            gap: var(--space-md);
            align-content: start;
        }

        .v03-header-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: var(--space-lg);
            border-bottom: 1px solid rgba(255,255,255,0.05);
            padding-bottom: var(--space-md);
        }

        .v03-insight-panel {
            background: var(--bg-surface-elevated);
            border-left: 3px solid var(--acc-cyan);
            padding: var(--space-md);
            font-family: var(--font-mono);
            font-size: 0.85rem;
            color: var(--text-secondary);
            display: flex;
            flex-direction: column;
            justify-content: center;
            opacity: 0.8;
            transition: opacity var(--duration-medium);
        }

        /* Sankey SVG Container */
        .v03-sankey-container {
            width: 100%;
            height: 65vh;
            position: relative;
            background: radial-gradient(ellipse at top, var(--bg-surface) 0%, transparent 80%);
            border-radius: 8px;
            overflow: hidden;
        }

        /* Sankey Nodes */
        .v03-sankey-node {
            fill: var(--bg-surface-elevated);
            stroke: var(--text-tertiary);
            stroke-width: 1;
            transition: stroke var(--duration-fast), fill var(--duration-fast);
        }

        .v03-sankey-node.is-active {
            stroke: var(--acc-cyan);
            fill: rgba(0, 240, 255, 0.05);
            filter: drop-shadow(0 0 10px var(--acc-cyan-glow));
        }

        /* Sankey Links (Paths) */
        .v03-sankey-link {
            fill: none;
            stroke-opacity: 0.15;
            transition: stroke-opacity var(--duration-medium), stroke var(--duration-medium);
            cursor: pointer;
        }
        
        .v03-sankey-link.flow-loss { stroke: var(--acc-amber); }
        .v03-sankey-link.flow-main { stroke: var(--acc-cyan); }
        
        .v03-sankey-link.is-active {
            stroke-opacity: 0.6;
            animation: flowDash 30s linear infinite;
            stroke-dasharray: 10 5;
        }

        @keyframes flowDash {
            to { stroke-dashoffset: -200; }
        }

        /* Typography inside SVG */
        .v03-node-label {
            font-family: var(--font-sans);
            font-size: 14px;
            fill: var(--text-secondary);
            font-weight: 300;
            transition: fill var(--duration-fast);
        }
        
        .v03-node-value {
            font-family: var(--font-mono);
            font-size: 18px;
            fill: var(--text-primary);
        }

        .is-active .v03-node-label {
            fill: var(--acc-cyan);
        }
        
        /* Metric Readout Transitions */
        .v03-metric-update {
            animation: textFlicker 0.3s ease-out forwards;
        }
        
        @keyframes textFlicker {
            0% { opacity: 0; transform: translateY(5px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        """

    def build_js(self) -> str:
        """Isolierter Controller für View 03 (Sankey Navigation & Data Update)."""
        return f"""
        /* ==========================================================================
           VIEW 03 CONTROLLER: SANKEY VALUE STREAM NAVIGATION
           ========================================================================== */
        class View03Controller {{
            constructor() {{
                this.viewElement = document.getElementById('{self.view_id}');
                this.stages = {json.dumps(self.flow_stages)};
                this.currentIndex = 0;
                
                this.initEvents();
            }}

            initEvents() {{
                window.addEventListener('keydown', (e) => {{
                    if (!this.viewElement || !this.viewElement.classList.contains('is-active')) return;

                    if (e.key === 'ArrowRight') {{
                        e.stopPropagation();
                        this.switchStage(1);
                    }} else if (e.key === 'ArrowLeft') {{
                        e.stopPropagation();
                        this.switchStage(-1);
                    }}
                }}, true); 
            }}

            switchStage(direction) {{
                this.currentIndex += direction;
                if (this.currentIndex >= this.stages.length) this.currentIndex = 0;
                if (this.currentIndex < 0) this.currentIndex = this.stages.length - 1;
                
                this.renderState();
            }}

            renderState() {{
                const stage = this.stages[this.currentIndex];

                // Update Header Metrics
                const insightEl = document.getElementById('v03-insight-text');
                const titleEl = document.getElementById('v03-active-stage');
                
                // Trigger reflow for animation
                insightEl.classList.remove('v03-metric-update');
                titleEl.classList.remove('v03-metric-update');
                void insightEl.offsetWidth; 
                
                insightEl.innerText = `> DS_LOG: ${{stage.ds_insight}}`;
                titleEl.innerText = `Focus: ${{stage.stage}}`;
                
                insightEl.classList.add('v03-metric-update');
                titleEl.classList.add('v03-metric-update');

                // Update SVG Nodes and Links
                document.querySelectorAll('.v03-sankey-node, .v03-sankey-link, .v03-node-group').forEach(el => {{
                    el.classList.remove('is-active');
                }});

                // Activate current node
                const activeGroup = document.getElementById(stage.id);
                if (activeGroup) {{
                    activeGroup.classList.add('is-active');
                    activeGroup.querySelector('.v03-sankey-node').classList.add('is-active');
                }}

                // Logic to activate paths leading TO this node
                document.querySelectorAll('.v03-sankey-link').forEach(link => {{
                    if (link.dataset.target === stage.id || link.dataset.source === stage.id) {{
                        link.classList.add('is-active');
                    }}
                }});
            }}
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            window.V03Controller = new View03Controller();
            setTimeout(() => window.V03Controller.renderState(), 800);
        }});
        """

    def build_html(self) -> str:
        """Generiert das HTML für View 03 inkl. hochpräzisem SVG Sankey."""
        return """
        <section class="view-container" id="view-03">
            
            <style>
                {css_inject}
            </style>

            <div class="v03-header-grid">
                <div>
                    <h2 style="font-size: 2rem; font-weight: 300; margin-bottom: 0.5rem;">
                        Predictive Value Stream <span class="font-mono text-accent">(Sankey)</span>
                    </h2>
                    <p class="text-secondary" style="font-size: 0.9rem;">
                        Algorithmische Aufschlüsselung der Wertschöpfungskette. Erkennung von Effizienzverlusten (Leaks) in Echtzeit.
                        <br>Nutze <kbd class="font-mono text-primary" style="background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">&larr;</kbd> <kbd class="font-mono text-primary" style="background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">&rarr;</kbd> für granularen Fokus.
                    </p>
                </div>
                <div class="v03-insight-panel">
                    <div id="v03-active-stage" style="color: var(--text-primary); margin-bottom: 0.25rem;">Focus: Revenue</div>
                    <div id="v03-insight-text" class="text-accent">
                        > DS_LOG: ARIMA Model: Top-line outperforming baseline due to Q3 seasonal anomaly.
                    </div>
                </div>
            </div>

            <div class="v03-sankey-container">
                <svg width="100%" height="100%" viewBox="0 0 1000 500" preserveAspectRatio="xMidYMid meet">
                    
                    <defs>
                        <linearGradient id="flow-rev-gm" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="var(--acc-cyan)"/>
                            <stop offset="100%" stop-color="var(--acc-cyan)"/>
                        </linearGradient>
                        <linearGradient id="flow-loss" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="var(--acc-cyan)"/>
                            <stop offset="100%" stop-color="var(--acc-amber)"/>
                        </linearGradient>
                    </defs>

                    <path class="v03-sankey-link flow-main is-active" data-source="node-rev" data-target="node-gm" 
                          stroke-width="140" d="M 150 250 C 350 250, 350 200, 500 200" />
                    
                    <path class="v03-sankey-link flow-loss is-active" data-source="node-rev" data-target="node-cogs" 
                          stroke-width="60" d="M 150 250 C 350 250, 350 400, 500 400" />

                    <path class="v03-sankey-link flow-main" data-source="node-gm" data-target="node-ebitda" 
                          stroke-width="80" d="M 550 200 C 700 200, 700 150, 850 150" />
                          
                    <path class="v03-sankey-link flow-loss" data-source="node-gm" data-target="node-opex" 
                          stroke-width="50" d="M 550 200 C 700 200, 700 300, 850 300" />

                    <path class="v03-sankey-link flow-main" data-source="node-ebitda" data-target="node-ni" 
                          stroke-width="50" d="M 900 150 C 950 150, 950 100, 1000 100" />

                    <g id="node-rev" class="v03-node-group is-active">
                        <rect class="v03-sankey-node is-active" x="100" y="150" width="50" height="200" rx="4" />
                        <text class="v03-node-label" x="90" y="240" text-anchor="end">Revenue</text>
                        <text class="v03-node-value" x="90" y="265" text-anchor="end">€240.5M</text>
                    </g>

                    <g id="node-gm" class="v03-node-group">
                        <rect class="v03-sankey-node" x="500" y="130" width="50" height="140" rx="4" />
                        <text class="v03-node-label" x="490" y="190" text-anchor="end">Gross Margin</text>
                        <text class="v03-node-value" x="490" y="215" text-anchor="end">€168.3M</text>
                    </g>

                    <g id="node-cogs" class="v03-node-group">
                        <rect class="v03-sankey-node" style="stroke: var(--acc-amber);" x="500" y="370" width="50" height="60" rx="4" />
                        <text class="v03-node-label" x="490" y="400" text-anchor="end">COGS</text>
                        <text class="v03-node-value" style="fill: var(--acc-amber);" x="490" y="420" text-anchor="end">€72.2M</text>
                    </g>

                    <g id="node-ebitda" class="v03-node-group">
                        <rect class="v03-sankey-node" x="850" y="110" width="50" height="80" rx="4" />
                        <text class="v03-node-label" x="840" y="145" text-anchor="end">EBITDA</text>
                        <text class="v03-node-value" x="840" y="165" text-anchor="end">€95.2M</text>
                    </g>

                    <g id="node-opex" class="v03-node-group">
                        <rect class="v03-sankey-node" style="stroke: var(--acc-amber);" x="850" y="275" width="50" height="50" rx="4" />
                        <text class="v03-node-label" x="840" y="300" text-anchor="end">OPEX</text>
                        <text class="v03-node-value" style="fill: var(--acc-amber);" x="840" y="320" text-anchor="end">€73.1M</text>
                    </g>

                    <line x1="125" y1="50" x2="125" y2="450" stroke="rgba(255,255,255,0.05)" stroke-dasharray="4" />
                    <line x1="525" y1="50" x2="525" y2="450" stroke="rgba(255,255,255,0.05)" stroke-dasharray="4" />
                    <line x1="875" y1="50" x2="875" y2="450" stroke="rgba(255,255,255,0.05)" stroke-dasharray="4" />
                    
                    <text x="125" y="40" class="v03-node-label" text-anchor="middle" style="font-size: 10px; text-transform: uppercase; letter-spacing: 2px;">Tier 1: Input</text>
                    <text x="525" y="40" class="v03-node-label" text-anchor="middle" style="font-size: 10px; text-transform: uppercase; letter-spacing: 2px;">Tier 2: Core</text>
                    <text x="875" y="40" class="v03-node-label" text-anchor="middle" style="font-size: 10px; text-transform: uppercase; letter-spacing: 2px;">Tier 3: Yield</text>

                </svg>
            </div>

            <script>
                {js_inject}
            </script>
        </section>
        """.replace("{css_inject}", self.build_css()).replace("{js_inject}", self.build_js())

    def get_output(self) -> str:
        return self.build_html()

if __name__ == "__main__":
    builder = CashflowSankeyBuilder()
    html_output = builder.get_output()
    print(html_output)