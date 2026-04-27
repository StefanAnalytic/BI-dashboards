# ==============================================================================
# DATEINAME: 04_predictive_ebitda.py
# VIEW: 04 - Machine Learning Forecast & Scenario Stress Testing
# ==============================================================================
"""
Dieses Skript generiert die vierte Ansichtsseite (View 04).
Es implementiert eine interaktive Machine-Learning-Zeitreihenanalyse (EBITDA Forecast).
Das Highlight ist ein SVG-basierter Chart mit Morphing-Animationen für das 
Konfidenzintervall (Shaded Area), abhängig vom gewählten Stresstest-Szenario.
Pfeiltasten LINKS/RECHTS wechseln zwischen den makroökonomischen ML-Szenarien.
"""

import json

class PredictiveForecastBuilder:
    def __init__(self):
        self.view_id = "view-04"
        
        # High-End Data Payload für die Zeitreihe (ARIMA / Prophet Mockup)
        # Die y-Werte sind SVG-Koordinaten (0 = top, 100 = bottom für einfaches Mapping)
        self.scenarios = [
            {
                "id": "baseline",
                "name": "Baseline (ARIMA + Seasonality)",
                "color": "var(--acc-cyan)",
                "kpi_ebitda": "€95.2M",
                "kpi_prob": "85%",
                "insight": "Normales Marktwachstum. Saisonale Q4-Spitze antizipiert.",
                # Forecast Line
                "path": "M 500 50 C 600 45, 700 30, 800 40 C 900 50, 950 20, 1000 25",
                # Confidence Interval (Polygon)
                "area": "M 500 50 C 600 35, 700 20, 800 25 C 900 35, 950 10, 1000 15 L 1000 45 C 950 40, 900 65, 800 60 C 700 50, 600 60, 500 50 Z"
            },
            {
                "id": "stress_inflation",
                "name": "Stress: High Inflation Overlay",
                "color": "var(--acc-amber)",
                "kpi_ebitda": "€78.4M",
                "kpi_prob": "12%",
                "insight": "OPEX-Eskalation durch 8% Inflation. Margenkompression in Q3.",
                "path": "M 500 50 C 600 60, 700 70, 800 65 C 900 80, 950 75, 1000 85",
                "area": "M 500 50 C 600 45, 700 55, 800 50 C 900 65, 950 60, 1000 70 L 1000 100 C 950 95, 900 100, 800 85 C 700 90, 600 80, 500 50 Z"
            },
            {
                "id": "stress_supply",
                "name": "Stress: Supply Chain Shock",
                "color": "var(--acc-red)",
                "kpi_ebitda": "€54.1M",
                "kpi_prob": "3%",
                "insight": "Starker COGS-Anstieg + Inventar-Engpass. Kritische Liquiditätswarnung.",
                "path": "M 500 50 C 600 80, 700 110, 800 130 C 900 140, 950 160, 1000 170",
                "area": "M 500 50 C 600 65, 700 90, 800 110 C 900 120, 950 140, 1000 150 L 1000 190 C 950 180, 900 170, 800 155 C 700 135, 600 105, 500 50 Z"
            }
        ]

    def build_css(self) -> str:
        """CSS für Chart-Morphing und Data-Visualisierung."""
        return """
        /* ==========================================================================
           VIEW 04: PREDICTIVE FORECAST STYLES
           ========================================================================== */
        #view-04 {
            display: grid;
            grid-template-columns: 1fr;
            grid-template-rows: auto auto 1fr;
            gap: var(--space-md);
        }

        /* Top Panel: Scenario Selector */
        .v04-scenario-bar {
            display: flex;
            gap: var(--space-md);
            border-bottom: 1px solid rgba(255,255,255,0.05);
            padding-bottom: var(--space-md);
        }

        .v04-scenario-btn {
            background: var(--bg-surface);
            border: 1px solid rgba(255,255,255,0.1);
            color: var(--text-secondary);
            padding: var(--space-sm) var(--space-md);
            font-family: var(--font-mono);
            font-size: 0.8rem;
            cursor: pointer;
            border-radius: 4px;
            transition: all var(--duration-fast);
            flex: 1;
            text-align: left;
            position: relative;
            overflow: hidden;
        }

        .v04-scenario-btn::before {
            content: '';
            position: absolute;
            left: 0; top: 0; bottom: 0; width: 3px;
            background: transparent;
            transition: background var(--duration-fast);
        }

        .v04-scenario-btn.is-active {
            background: var(--bg-surface-elevated);
            color: var(--text-primary);
            border-color: rgba(255,255,255,0.2);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        }

        .v04-scenario-btn.is-active[data-scenario="0"]::before { background: var(--acc-cyan); }
        .v04-scenario-btn.is-active[data-scenario="1"]::before { background: var(--acc-amber); }
        .v04-scenario-btn.is-active[data-scenario="2"]::before { background: var(--acc-red); }

        /* Chart Area */
        .v04-chart-container {
            width: 100%;
            height: 55vh;
            background: var(--bg-surface);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 8px;
            position: relative;
            overflow: hidden;
            padding: var(--space-md);
        }

        /* SVG Paths with Morphing CSS Transitions */
        .v04-chart-svg {
            width: 100%;
            height: 100%;
            overflow: visible;
        }

        .v04-path-history {
            fill: none;
            stroke: var(--text-primary);
            stroke-width: 3;
            stroke-linecap: round;
            filter: drop-shadow(0 0 5px rgba(255,255,255,0.3));
        }

        .v04-path-forecast {
            fill: none;
            stroke-width: 3;
            stroke-dasharray: 8 6;
            stroke-linecap: round;
            transition: d var(--duration-slow) var(--ease-in-out-circ),
                        stroke var(--duration-slow);
        }

        .v04-area-forecast {
            transition: d var(--duration-slow) var(--ease-in-out-circ),
                        fill var(--duration-slow);
            opacity: 0.15;
        }

        /* Data Tooltip overlay */
        .v04-data-overlay {
            position: absolute;
            top: var(--space-md);
            right: var(--space-md);
            background: var(--bg-glass);
            border: 1px solid rgba(255,255,255,0.1);
            padding: var(--space-md);
            border-radius: 4px;
            min-width: 250px;
            backdrop-filter: blur(8px);
        }
        
        .v04-divider-line {
            stroke: var(--text-tertiary);
            stroke-width: 1;
            stroke-dasharray: 4;
        }
        """

    def build_js(self) -> str:
        """Controller für Morphing und Daten-Updates in View 04."""
        return f"""
        /* ==========================================================================
           VIEW 04 CONTROLLER: TIME-SERIES MORPHING & STRESS TESTS
           ========================================================================== */
        class View04Controller {{
            constructor() {{
                this.viewElement = document.getElementById('{self.view_id}');
                this.scenarios = {json.dumps(self.scenarios)};
                this.currentIndex = 0;
                
                this.pathEl = document.getElementById('v04-forecast-line');
                this.areaEl = document.getElementById('v04-forecast-area');
                
                this.initEvents();
            }}

            initEvents() {{
                window.addEventListener('keydown', (e) => {{
                    if (!this.viewElement || !this.viewElement.classList.contains('is-active')) return;

                    if (e.key === 'ArrowRight') {{
                        e.stopPropagation();
                        this.switchScenario(1);
                    }} else if (e.key === 'ArrowLeft') {{
                        e.stopPropagation();
                        this.switchScenario(-1);
                    }}
                }}, true); 
            }}

            switchScenario(direction) {{
                this.currentIndex += direction;
                if (this.currentIndex >= this.scenarios.length) this.currentIndex = 0;
                if (this.currentIndex < 0) this.currentIndex = this.scenarios.length - 1;
                
                this.renderState();
            }}

            renderState() {{
                const data = this.scenarios[this.currentIndex];

                // Update UI Buttons
                document.querySelectorAll('.v04-scenario-btn').forEach((btn, idx) => {{
                    btn.classList.toggle('is-active', idx === this.currentIndex);
                }});

                // Update Overlay Text
                document.getElementById('v04-val-ebitda').innerText = data.kpi_ebitda;
                document.getElementById('v04-val-ebitda').style.color = data.color;
                
                document.getElementById('v04-val-prob').innerText = data.kpi_prob;
                document.getElementById('v04-val-insight').innerText = data.insight;

                // Morph SVG Paths natively via CSS transition on the 'd' attribute
                if (this.pathEl && this.areaEl) {{
                    this.pathEl.setAttribute('d', data.path);
                    this.pathEl.style.stroke = data.color;
                    
                    this.areaEl.setAttribute('d', data.area);
                    this.areaEl.style.fill = data.color;
                }}
            }}
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            window.V04Controller = new View04Controller();
            setTimeout(() => window.V04Controller.renderState(), 1000);
        }});
        """

    def build_html(self) -> str:
        """Generiert das HTML für View 04 inkl. Morphing-SVG."""
        return """
        <section class="view-container" id="view-04">
            
            <style>
                {css_inject}
            </style>

            <div class="v04-header">
                <h2 style="font-size: 2rem; font-weight: 300; margin-bottom: 0.5rem;">
                    EBITDA <span class="font-mono text-accent">Predictive Trajectory</span>
                </h2>
                <p class="text-secondary" style="font-size: 0.9rem;">
                    Zeitreihenprognose (Prophet Model) mit 95% Konfidenzintervallen.
                    Schalte makroökonomische Stresstests mit <kbd class="font-mono text-primary" style="background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">&larr;</kbd> <kbd class="font-mono text-primary" style="background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">&rarr;</kbd> um.
                </p>
            </div>

            <div class="v04-scenario-bar">
                <button class="v04-scenario-btn is-active" data-scenario="0">
                    <div style="font-size: 0.7rem; color: var(--text-tertiary); margin-bottom: 4px;">SCENARIO 01</div>
                    <div>Baseline Vector</div>
                </button>
                <button class="v04-scenario-btn" data-scenario="1">
                    <div style="font-size: 0.7rem; color: var(--text-tertiary); margin-bottom: 4px;">SCENARIO 02</div>
                    <div>Inflation Shock Overlay</div>
                </button>
                <button class="v04-scenario-btn" data-scenario="2">
                    <div style="font-size: 0.7rem; color: var(--text-tertiary); margin-bottom: 4px;">SCENARIO 03</div>
                    <div>Supply Chain Crisis</div>
                </button>
            </div>

            <div class="v04-chart-container">
                
                <div class="v04-data-overlay">
                    <div class="kpi-label">Projected Q4 EBITDA</div>
                    <div class="kpi-value" id="v04-val-ebitda" style="font-size: 2.5rem; color: var(--acc-cyan); margin-bottom: var(--space-sm);">€95.2M</div>
                    
                    <div style="display: flex; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.1); padding-top: var(--space-sm); margin-bottom: var(--space-sm);">
                        <span class="text-secondary" style="font-size: 0.8rem;">Model Confidence</span>
                        <span class="font-mono" id="v04-val-prob">85%</span>
                    </div>
                    
                    <div class="text-secondary font-mono" id="v04-val-insight" style="font-size: 0.75rem; line-height: 1.4;">
                        Normales Marktwachstum. Saisonale Q4-Spitze antizipiert.
                    </div>
                </div>

                <svg class="v04-chart-svg" viewBox="0 0 1000 250" preserveAspectRatio="none">
                    
                    <g stroke="rgba(255,255,255,0.03)" stroke-width="1">
                        <line x1="0" y1="50" x2="1000" y2="50" />
                        <line x1="0" y1="100" x2="1000" y2="100" />
                        <line x1="0" y1="150" x2="1000" y2="150" />
                        <line x1="0" y1="200" x2="1000" y2="200" />
                    </g>

                    <line class="v04-divider-line" x1="500" y1="0" x2="500" y2="250" />
                    <text x="490" y="20" fill="var(--text-tertiary)" font-family="var(--font-mono)" font-size="12" text-anchor="end">Historical Actuals</text>
                    <text x="510" y="20" fill="var(--acc-cyan)" font-family="var(--font-mono)" font-size="12" text-anchor="start">ML Forecast Area</text>

                    <path class="v04-path-history" d="M 0 180 Q 100 170, 200 150 T 400 100 T 500 50" />
                    
                    <path id="v04-forecast-area" class="v04-area-forecast" fill="var(--acc-cyan)" 
                          d="M 500 50 C 600 35, 700 20, 800 25 C 900 35, 950 10, 1000 15 L 1000 45 C 950 40, 900 65, 800 60 C 700 50, 600 60, 500 50 Z" />

                    <path id="v04-forecast-line" class="v04-path-forecast" stroke="var(--acc-cyan)" 
                          d="M 500 50 C 600 45, 700 30, 800 40 C 900 50, 950 20, 1000 25" />
                          
                    <circle cx="500" cy="50" r="4" fill="var(--bg-surface)" stroke="var(--text-primary)" stroke-width="2" />
                    
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
    builder = PredictiveForecastBuilder()
    html_output = builder.get_output()
    print(html_output)