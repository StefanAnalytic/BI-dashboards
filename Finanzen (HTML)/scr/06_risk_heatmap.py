# ==============================================================================
# DATEINAME: 06_risk_heatmap.py
# VIEW: 06 - Monte Carlo Risk Heatmap & Probability Density
# ==============================================================================
"""
Dieses Skript generiert die sechste Ansichtsseite (View 06).
Es implementiert eine 3x3 Risikomatrix (Likelihood vs. Impact), hinterlegt mit 
den Ergebnissen einer stochastischen Monte-Carlo-Simulation (N=10.000).
Die Pfeiltasten LINKS/RECHTS navigieren flüssig durch die einzelnen Risikozellen,
wodurch dynamische Probability Density Functions (PDF-Charts) gezeichnet werden.
"""

import json

class MonteCarloRiskBuilder:
    def __init__(self):
        self.view_id = "view-06"
        
        # High-End Data Payload (3x3 Matrix Grid)
        # Position: [Likelihood (1-3), Impact (1-3)] - 3 is highest
        self.risk_data = [
            {"id": "R1", "pos": [3, 3], "name": "FX Exposure (USD/EUR)", "status": "Critical", "color": "var(--acc-red)", "var": "€18.2M", "insight": "Hohe Volatilität antizipiert. Hedging-Quote aktuell bei nur 42%.", "path": "M 0 100 Q 20 100, 40 80 T 100 20 T 160 80 Q 180 100, 200 100"},
            {"id": "R2", "pos": [2, 3], "name": "Supply Chain APAC", "status": "High", "color": "var(--acc-red)", "var": "€14.5M", "insight": "Korrelation mit Transportkosten-Index (Baltic Dry).", "path": "M 0 100 Q 30 100, 60 90 T 120 40 T 160 80 Q 180 100, 200 100"},
            {"id": "R3", "pos": [3, 2], "name": "Interest Rate Hike", "status": "High", "color": "var(--acc-amber)", "var": "€9.1M", "insight": "EZB-Zinsentscheid eingepreist, aber Restrisiko im variabel verzinsten Portfolio.", "path": "M 0 100 Q 40 100, 70 70 T 130 50 T 170 90 Q 185 100, 200 100"},
            {"id": "R4", "pos": [1, 3], "name": "Cyber / IT Outage", "status": "Medium", "color": "var(--acc-amber)", "var": "€22.0M", "insight": "Geringe Wahrscheinlichkeit, aber fatales Tail-Risk (Black Swan).", "path": "M 0 100 L 140 100 L 150 10 L 160 100 L 200 100"},
            {"id": "R5", "pos": [2, 2], "name": "Commodity (Copper)", "status": "Medium", "color": "var(--acc-amber)", "var": "€6.4M", "insight": "Termingeschäfte decken Q3, Q4 ist ungesichert.", "path": "M 0 100 Q 50 100, 80 60 T 140 60 Q 170 100, 200 100"},
            {"id": "R6", "pos": [1, 2], "name": "Labor Cost Inflation", "status": "Low", "color": "var(--acc-cyan)", "var": "€4.2M", "insight": "Tarifverträge bis 2026 fixiert. Geringes Restrisiko durch Boni.", "path": "M 0 100 Q 50 100, 100 80 T 150 90 Q 180 100, 200 100"}
        ]

    def build_css(self) -> str:
        """CSS für die 3x3 Heatmap und PDF (Probability Density Function) Charts."""
        return """
        /* ==========================================================================
           VIEW 06: MONTE CARLO HEATMAP STYLES
           ========================================================================== */
        #view-06 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-gap: var(--space-xl);
            align-items: center;
        }

        .v06-content-left {
            display: flex;
            flex-direction: column;
            gap: var(--space-md);
            height: 100%;
            justify-content: center;
        }

        .v06-content-right {
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* 3x3 Heatmap Grid */
        .v06-heatmap {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            grid-template-rows: repeat(3, 1fr);
            gap: var(--space-sm);
            width: 100%;
            max-width: 500px;
            aspect-ratio: 1;
            position: relative;
            background: var(--bg-surface);
            padding: var(--space-md);
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.05);
        }

        /* Axis Labels */
        .v06-axis-y {
            position: absolute;
            left: -40px;
            top: 50%;
            transform: translateY(-50%) rotate(-90deg);
            font-family: var(--font-mono);
            font-size: 0.75rem;
            color: var(--text-tertiary);
            letter-spacing: 0.1em;
        }

        .v06-axis-x {
            position: absolute;
            bottom: -30px;
            left: 50%;
            transform: translateX(-50%);
            font-family: var(--font-mono);
            font-size: 0.75rem;
            color: var(--text-tertiary);
            letter-spacing: 0.1em;
        }

        /* Heatmap Cells */
        .v06-cell {
            background: var(--bg-surface-elevated);
            border-radius: 4px;
            border: 1px solid rgba(255,255,255,0.02);
            position: relative;
            transition: all var(--duration-fast);
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* Grid Placement: Row 1 is Top (Likelihood 3), Col 3 is Right (Impact 3) */
        .v06-cell[data-pos="3-1"] { grid-row: 1; grid-column: 1; }
        .v06-cell[data-pos="3-2"] { grid-row: 1; grid-column: 2; }
        .v06-cell[data-pos="3-3"] { grid-row: 1; grid-column: 3; background: rgba(255, 51, 102, 0.1); }
        
        .v06-cell[data-pos="2-1"] { grid-row: 2; grid-column: 1; }
        .v06-cell[data-pos="2-2"] { grid-row: 2; grid-column: 2; }
        .v06-cell[data-pos="2-3"] { grid-row: 2; grid-column: 3; }
        
        .v06-cell[data-pos="1-1"] { grid-row: 3; grid-column: 1; background: rgba(0, 230, 118, 0.05); }
        .v06-cell[data-pos="1-2"] { grid-row: 3; grid-column: 2; }
        .v06-cell[data-pos="1-3"] { grid-row: 3; grid-column: 3; }

        /* Nodes within cells */
        .v06-node {
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: var(--text-tertiary);
            position: absolute;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
            transition: all var(--duration-fast);
            cursor: pointer;
        }

        .v06-node.is-active {
            transform: scale(1.5);
            background: var(--node-color, var(--acc-cyan));
            box-shadow: 0 0 15px var(--node-color, var(--acc-cyan));
            border: 2px solid #fff;
            z-index: 10;
        }

        /* Distribution Chart (PDF) */
        .v06-pdf-chart {
            width: 100%;
            height: 150px;
            margin-top: var(--space-md);
            position: relative;
            border-bottom: 1px solid var(--text-tertiary);
            overflow: visible;
        }

        .v06-pdf-path {
            fill: var(--chart-fill, rgba(255,255,255,0.1));
            stroke: var(--chart-stroke, var(--text-secondary));
            stroke-width: 2;
            transition: d 0.6s var(--ease-out-expo), fill 0.6s, stroke 0.6s;
        }

        /* VaR Indicator Line */
        .v06-var-line {
            position: absolute;
            top: 0; bottom: 0;
            width: 2px;
            background: var(--acc-red);
            right: 20%;
            opacity: 0.5;
            border-left: 1px dashed #fff;
        }
        
        .v06-var-label {
            position: absolute;
            top: -20px;
            right: 20%;
            transform: translateX(50%);
            font-family: var(--font-mono);
            font-size: 0.7rem;
            color: var(--acc-red);
        }
        """

    def build_js(self) -> str:
        """Controller für View 06: Heatmap Navigation & PDF Rendering."""
        return f"""
        /* ==========================================================================
           VIEW 06 CONTROLLER: MONTE CARLO MATRIX NAVIGATOR
           ========================================================================== */
        class View06Controller {{
            constructor() {{
                this.viewElement = document.getElementById('{self.view_id}');
                this.risks = {json.dumps(self.risk_data)};
                this.currentIndex = 0;
                
                this.pdfPathEl = document.getElementById('v06-pdf-path');
                
                this.initEvents();
            }}

            initEvents() {{
                window.addEventListener('keydown', (e) => {{
                    if (!this.viewElement || !this.viewElement.classList.contains('is-active')) return;

                    if (e.key === 'ArrowRight') {{
                        e.stopPropagation();
                        this.switchRisk(1);
                    }} else if (e.key === 'ArrowLeft') {{
                        e.stopPropagation();
                        this.switchRisk(-1);
                    }}
                }}, true);
            }}

            switchRisk(direction) {{
                this.currentIndex += direction;
                if (this.currentIndex >= this.risks.length) this.currentIndex = 0;
                if (this.currentIndex < 0) this.currentIndex = this.risks.length - 1;
                
                this.renderState();
            }}

            renderState() {{
                const data = this.risks[this.currentIndex];

                // Update text elements
                document.getElementById('v06-risk-title').innerText = data.name;
                document.getElementById('v06-risk-title').style.color = data.color;
                
                document.getElementById('v06-risk-var').innerText = data.var;
                document.getElementById('v06-risk-var').style.color = data.color;
                
                document.getElementById('v06-risk-insight').innerText = '> ' + data.insight;

                // Update Matrix Nodes
                document.querySelectorAll('.v06-node').forEach((node) => {{
                    if (node.dataset.id === data.id) {{
                        node.classList.add('is-active');
                        node.style.setProperty('--node-color', data.color);
                    }} else {{
                        node.classList.remove('is-active');
                    }}
                }});

                // Morph PDF Chart
                if (this.pdfPathEl) {{
                    // Add the bottom closing coordinates for a filled path
                    const closedPath = data.path + ' L 200 120 L 0 120 Z';
                    this.pdfPathEl.setAttribute('d', closedPath);
                    
                    // Update CSS variables for colors
                    this.pdfPathEl.style.setProperty('--chart-stroke', data.color);
                    // Convert hex/var to rgba for fill
                    this.pdfPathEl.style.setProperty('--chart-fill', data.color === 'var(--acc-red)' ? 'rgba(255, 51, 102, 0.15)' : 
                                                                     data.color === 'var(--acc-amber)' ? 'rgba(255, 176, 0, 0.15)' : 
                                                                     'rgba(0, 240, 255, 0.15)');
                }}
            }}
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            window.V06Controller = new View06Controller();
            setTimeout(() => window.V06Controller.renderState(), 1400);
        }});
        """

    def build_html(self) -> str:
        """Generiert das HTML für View 06 (Heatmap + Data Overlay)."""
        
        # Dynamisch die Nodes in die passenden Zellen generieren
        cells_html = ""
        for likelihood in range(3, 0, -1):
            for impact in range(1, 4):
                pos = f"{likelihood}-{impact}"
                nodes_in_cell = ""
                
                # Suchen, ob Risiken in diese Zelle fallen
                for risk in self.risk_data:
                    if risk["pos"] == [likelihood, impact]:
                        # Füge Node hinzu (mit leichtem Offset bei mehreren in einer Zelle, falls nötig)
                        nodes_in_cell += f'<div class="v06-node" data-id="{risk["id"]}"></div>'

                cells_html += f'<div class="v06-cell" data-pos="{pos}">{nodes_in_cell}</div>\n'

        return f"""
        <section class="view-container" id="view-06">
            
            <style>
                {self.build_css()}
            </style>

            <div class="v06-content-left">
                <div>
                    <h2 style="font-size: 2rem; font-weight: 300; margin-bottom: 0.5rem;">
                        Stochastic <span class="font-mono text-accent">Risk Matrix</span>
                    </h2>
                    <p class="text-secondary" style="font-size: 0.9rem;">
                        Monte-Carlo-Simulation (10,000 Iterationen) mit Cholesky-Zerlegung zur Berücksichtigung von Kreuzkorrelationen (z.B. FX & Supply Chain). 
                        Fokus wechseln mit <kbd class="font-mono text-primary" style="background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">&larr;</kbd> <kbd class="font-mono text-primary" style="background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">&rarr;</kbd>.
                    </p>
                </div>

                <div class="kpi-card" style="margin-top: var(--space-md);">
                    <div class="kpi-label" style="display: flex; justify-content: space-between;">
                        <span>Selected Risk Vector</span>
                        <span class="font-mono" style="color: var(--text-tertiary);">N=10,000</span>
                    </div>
                    <h3 id="v06-risk-title" style="font-size: 1.5rem; margin-bottom: var(--space-sm); color: var(--acc-red);">FX Exposure (USD/EUR)</h3>
                    
                    <div style="display: flex; align-items: baseline; gap: var(--space-md); border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: var(--space-md); margin-bottom: var(--space-sm);">
                        <div>
                            <div class="text-secondary font-mono" style="font-size: 0.7rem;">95% CVaR (Tail Risk)</div>
                            <div id="v06-risk-var" class="font-mono" style="font-size: 2rem; color: var(--acc-red);">€18.2M</div>
                        </div>
                    </div>

                    <div id="v06-risk-insight" class="font-mono text-secondary" style="font-size: 0.8rem; line-height: 1.5;">
                        > Hohe Volatilität antizipiert. Hedging-Quote aktuell bei nur 42%.
                    </div>

                    <div style="margin-top: var(--space-lg);">
                        <div class="text-secondary font-mono" style="font-size: 0.7rem; margin-bottom: 8px;">Probability Density Function (PDF)</div>
                        <div class="v06-pdf-chart">
                            <div class="v06-var-label">95% CI</div>
                            <div class="v06-var-line"></div>
                            <svg viewBox="0 0 200 120" preserveAspectRatio="none" style="width: 100%; height: 100%;">
                                <path id="v06-pdf-path" class="v06-pdf-path" d="M 0 100 Q 20 100, 40 80 T 100 20 T 160 80 Q 180 100, 200 100 L 200 120 L 0 120 Z" />
                            </svg>
                        </div>
                    </div>
                </div>
            </div>

            <div class="v06-content-right">
                <div class="v06-heatmap">
                    <div class="v06-axis-y">LIKELIHOOD &rarr;</div>
                    <div class="v06-axis-x">IMPACT &rarr;</div>
                    
                    {cells_html}
                </div>
            </div>

            <script>
                {self.build_js()}
            </script>
        </section>
        """

    def get_output(self) -> str:
        return self.build_html()

if __name__ == "__main__":
    builder = MonteCarloRiskBuilder()
    html_output = builder.get_output()
    print(html_output)