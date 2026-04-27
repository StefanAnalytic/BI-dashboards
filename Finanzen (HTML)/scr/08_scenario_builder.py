# ==============================================================================
# DATEINAME: 08_scenario_builder.py
# VIEW: 08 - Interactive 'What-If' Sandbox (CFO Control Panel)
# ==============================================================================
"""
Dieses Skript generiert die achte Ansichtsseite (View 08).
Es implementiert eine interaktive "What-If" Simulationsumgebung (Digital Twin),
in der makroökonomische und interne Hebel (Inflation, Zinsen, OPEX, Wachstum) 
justiert werden. Die Pfeiltasten LINKS/RECHTS wechseln zwischen vordefinierten, 
komplexen Makro-Szenarien, die als Seed-Werte für die Sliders fungieren.
Die JS-Engine berechnet in Echtzeit die Auswirkungen auf Kern-KPIs (FCF, Margin) 
basierend auf einer hinterlegten Elastizitäts-Matrix.
"""

import json

class SandboxScenarioBuilder:
    def __init__(self):
        self.view_id = "view-08"
        
        # High-End Data Payload: Makro-Szenarien & Elastizitäten
        # Base KPIs: FCF = 142.5, Margin = 34.0%, Valuation = 1250.0
        self.scenarios = [
            {
                "id": "baseline",
                "name": "Current Baseline Vector",
                "insight": "Modell operiert auf aktuellen Marktdaten. Keine Anomalien induziert.",
                "inputs": {"inflation": 2.5, "interest": 4.0, "opex": 0.0, "growth": 5.0}
            },
            {
                "id": "stagflation",
                "name": "Stress: Global Stagflation",
                "insight": "Hohe Inflation bei sinkendem Wachstum. Margenkompression greift aggressiv.",
                "inputs": {"inflation": 8.5, "interest": 6.5, "opex": 5.0, "growth": -2.0}
            },
            {
                "id": "expansion",
                "name": "Strategy: Aggressive Expansion",
                "insight": "Erhöhter OPEX-Spend treibt Top-Line, aber drückt kurzfristigen Free Cash Flow.",
                "inputs": {"inflation": 3.0, "interest": 3.5, "opex": 15.0, "growth": 18.0}
            },
            {
                "id": "efficiency",
                "name": "Strategy: AI Cost Optimization",
                "insight": "Automatisierung senkt OPEX drastisch. Margen-Expansion trotz flachem Wachstum.",
                "inputs": {"inflation": 2.5, "interest": 4.0, "opex": -12.0, "growth": 3.0}
            }
        ]
        
        # Basiswerte für die Berechnung (Hidden State)
        self.base_metrics = {"fcf": 142.5, "margin": 34.0, "valuation": 1250.0}

    def build_css(self) -> str:
        """CSS für Glassmorphism-Panels, Custom Range Sliders und SVG Gauges."""
        return """
        /* ==========================================================================
           VIEW 08: SCENARIO BUILDER STYLES
           ========================================================================== */
        #view-08 {
            display: grid;
            grid-template-columns: 400px 1fr;
            grid-gap: var(--space-xl);
            align-items: center;
        }

        .v08-control-panel {
            display: flex;
            flex-direction: column;
            gap: var(--space-md);
            background: var(--bg-surface);
            padding: var(--space-lg);
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.05);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            z-index: 2;
        }

        /* Custom Range Sliders */
        .v08-slider-group {
            display: flex;
            flex-direction: column;
            gap: var(--space-xs);
        }

        .v08-slider-header {
            display: flex;
            justify-content: space-between;
            font-family: var(--font-mono);
            font-size: 0.8rem;
            color: var(--text-secondary);
        }

        .v08-slider {
            -webkit-appearance: none;
            width: 100%;
            height: 4px;
            background: rgba(255,255,255,0.1);
            border-radius: 2px;
            outline: none;
            transition: background var(--duration-fast);
        }

        .v08-slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: var(--acc-cyan);
            cursor: pointer;
            box-shadow: 0 0 10px var(--acc-cyan-glow);
            transition: transform var(--duration-fast);
        }

        .v08-slider::-webkit-slider-thumb:hover {
            transform: scale(1.2);
        }
        
        /* Modifiers for different sliders */
        .v08-slider[data-type="risk"]::-webkit-slider-thumb { background: var(--acc-red); box-shadow: 0 0 10px rgba(255, 51, 102, 0.3); }
        .v08-slider[data-type="neutral"]::-webkit-slider-thumb { background: var(--acc-amber); box-shadow: 0 0 10px rgba(255, 176, 0, 0.3); }
        .v08-slider[data-type="growth"]::-webkit-slider-thumb { background: var(--acc-purple); box-shadow: 0 0 10px rgba(138, 43, 226, 0.3); }

        /* Output Dashboard Area */
        .v08-output-area {
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-template-rows: auto 1fr;
            gap: var(--space-lg);
            height: 100%;
        }

        .v08-scenario-header {
            grid-column: 1 / -1;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        /* Gauge Components */
        .v08-gauge-card {
            background: var(--bg-surface-elevated);
            border: 1px solid rgba(255,255,255,0.02);
            border-radius: 8px;
            padding: var(--space-lg);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
        }

        .v08-gauge-svg {
            width: 180px;
            height: 180px;
            transform: rotate(-90deg);
        }

        .v08-gauge-bg {
            fill: none;
            stroke: rgba(255,255,255,0.05);
            stroke-width: 8;
        }

        .v08-gauge-fill {
            fill: none;
            stroke: var(--gauge-color, var(--acc-cyan));
            stroke-width: 8;
            stroke-linecap: round;
            stroke-dasharray: 440; /* 2 * pi * r (r=70) */
            stroke-dashoffset: 440;
            transition: stroke-dashoffset 1s var(--ease-out-expo), stroke 0.5s;
        }

        .v08-gauge-content {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .v08-gauge-value {
            font-family: var(--font-mono);
            font-size: 2.5rem;
            color: var(--text-primary);
            transition: color 0.3s;
        }

        .v08-gauge-label {
            font-size: 0.75rem;
            color: var(--text-tertiary);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-top: 4px;
        }
        
        .v08-delta-badge {
            margin-top: 8px;
            font-family: var(--font-mono);
            font-size: 0.75rem;
            padding: 2px 8px;
            border-radius: 12px;
            background: rgba(255,255,255,0.05);
        }
        """

    def build_js(self) -> str:
        """Controller für View 08: Elastizitäts-Modellierung & Gauge-Animation."""
        return f"""
        /* ==========================================================================
           VIEW 08 CONTROLLER: DIGITAL TWIN SIMULATION ENGINE
           ========================================================================== */
        class View08Controller {{
            constructor() {{
                this.viewElement = document.getElementById('{self.view_id}');
                this.scenarios = {json.dumps(self.scenarios)};
                this.baseMetrics = {json.dumps(self.base_metrics)};
                this.currentIndex = 0;
                
                // DOM Elements
                this.sliders = {{
                    inflation: document.getElementById('v08-slide-inf'),
                    interest: document.getElementById('v08-slide-int'),
                    opex: document.getElementById('v08-slide-opx'),
                    growth: document.getElementById('v08-slide-grw')
                }};
                
                this.valDisplays = {{
                    inflation: document.getElementById('v08-val-inf'),
                    interest: document.getElementById('v08-val-int'),
                    opex: document.getElementById('v08-val-opx'),
                    growth: document.getElementById('v08-val-grw')
                }};

                this.initEvents();
            }}

            initEvents() {{
                // Keyboard Navigation for Scenarios
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

                // Slider Input Listeners for manual override
                Object.keys(this.sliders).forEach(key => {{
                    this.sliders[key].addEventListener('input', () => this.handleManualInput());
                }});
            }}

            switchScenario(direction) {{
                this.currentIndex += direction;
                if (this.currentIndex >= this.scenarios.length) this.currentIndex = 0;
                if (this.currentIndex < 0) this.currentIndex = this.scenarios.length - 1;
                
                this.loadScenario(this.scenarios[this.currentIndex]);
            }}

            loadScenario(scenario) {{
                // Update UI Header
                document.getElementById('v08-scen-title').innerText = scenario.name;
                document.getElementById('v08-scen-insight').innerText = '> DS_LOG: ' + scenario.insight;

                // Set Slider Values
                this.sliders.inflation.value = scenario.inputs.inflation;
                this.sliders.interest.value = scenario.inputs.interest;
                this.sliders.opex.value = scenario.inputs.opex;
                this.sliders.growth.value = scenario.inputs.growth;

                this.calculateModel();
            }}

            handleManualInput() {{
                document.getElementById('v08-scen-title').innerText = "Custom Simulation (Manual Override)";
                document.getElementById('v08-scen-insight').innerText = "> DS_LOG: Berechne Elastizitäten in Echtzeit...";
                this.calculateModel();
            }}

            calculateModel() {{
                // 1. Get current input values
                const inf = parseFloat(this.sliders.inflation.value);
                const int = parseFloat(this.sliders.interest.value);
                const opx = parseFloat(this.sliders.opex.value);
                const grw = parseFloat(this.sliders.growth.value);

                // Update Slider Displays
                this.valDisplays.inflation.innerText = inf.toFixed(1) + '%';
                this.valDisplays.interest.innerText = int.toFixed(1) + '%';
                this.valDisplays.opex.innerText = (opx > 0 ? '+' : '') + opx.toFixed(1) + '%';
                this.valDisplays.growth.innerText = (grw > 0 ? '+' : '') + grw.toFixed(1) + '%';

                // 2. Mathematical Elasticity Model (Pseudo-Data Science Logic)
                // FCF ist negativ korreliert mit Inflation, Zinsen, OPEX; positiv mit Growth.
                const fcf_multiplier = 1 - ((inf-2.5)*0.02) - ((int-4.0)*0.015) - (opx*0.012) + ((grw-5.0)*0.018);
                const newFcf = this.baseMetrics.fcf * fcf_multiplier;

                // Margin leidet stark unter Inflation und OPEX, profitiert von Effizienz (negativer OPEX).
                const margin_multiplier = 1 - ((inf-2.5)*0.03) - (opx*0.015) + ((grw-5.0)*0.005);
                const newMargin = this.baseMetrics.margin * margin_multiplier;

                // Valuation ist stark zinsabhängig (DCF-Logik) + FCF Wachstum.
                const val_multiplier = 1 - ((int-4.0)*0.08) + ((newFcf - this.baseMetrics.fcf)/this.baseMetrics.fcf)*0.4;
                const newVal = this.baseMetrics.valuation * val_multiplier;

                // 3. Render Output
                this.updateGauge('fcf', newFcf, this.baseMetrics.fcf, '€', 'M', 250); // Max gauge scale 250
                this.updateGauge('margin', newMargin, this.baseMetrics.margin, '', '%', 50); // Max scale 50
                this.updateGauge('val', newVal, this.baseMetrics.valuation, '€', 'B', 2000, 1000); // Format as Billions (val / 1000)
            }}

            updateGauge(id, current, base, prefix, suffix, maxScale, divideBy = 1) {{
                const displayVal = current / divideBy;
                const baseDisplay = base / divideBy;
                
                const delta = ((current - base) / base) * 100;
                
                // DOM Updates
                document.getElementById(`v08-val-${{id}}`).innerText = prefix + displayVal.toFixed(1) + suffix;
                
                const deltaEl = document.getElementById(`v08-delta-${{id}}`);
                deltaEl.innerText = (delta > 0 ? '+' : '') + delta.toFixed(1) + '% vs Base';
                
                // Color Logic
                let color = 'var(--acc-cyan)';
                if (delta < -10) color = 'var(--acc-red)';
                else if (delta < 0) color = 'var(--acc-amber)';
                else if (delta > 10) color = 'var(--acc-green)';

                deltaEl.style.color = color;
                
                // SVG Dash Array Logic (circumference = 440)
                const fillCircle = document.getElementById(`v08-fill-${{id}}`);
                const percentage = Math.max(0, Math.min(100, (current / maxScale) * 100));
                const dashOffset = 440 - (440 * (percentage / 100));
                
                fillCircle.style.setProperty('--gauge-color', color);
                fillCircle.style.strokeDashoffset = dashOffset;
            }}
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            window.V08Controller = new View08Controller();
            // Load initial scenario after short delay for animation
            setTimeout(() => window.V08Controller.loadScenario(window.V08Controller.scenarios[0]), 1800);
        }});
        """

    def build_html(self) -> str:
        """Generiert das HTML für View 08 (Control Panel + Gauges)."""
        return """
        <section class="view-container" id="view-08">
            
            <style>
                {css_inject}
            </style>

            <div class="v08-control-panel">
                <div>
                    <h2 style="font-size: 1.8rem; font-weight: 300; margin-bottom: 0.5rem;">
                        Digital Twin <span class="font-mono text-accent">Sandbox</span>
                    </h2>
                    <p class="text-secondary" style="font-size: 0.85rem; line-height: 1.5;">
                        Interaktive Manipulation makroökonomischer Vektoren. Das System berechnet die P&L-Elastizität in Echtzeit via multivariater Regression.
                    </p>
                </div>

                <div style="margin: var(--space-md) 0; padding-bottom: var(--space-md); border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <div class="kpi-label" style="display:flex; justify-content:space-between; align-items:center;">
                        <span>Macro Environment</span>
                        <div style="background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">
                            <kbd class="font-mono text-primary">&larr;</kbd> <kbd class="font-mono text-primary">&rarr;</kbd>
                        </div>
                    </div>
                    
                    <div class="v08-slider-group" style="margin-top: var(--space-md);">
                        <div class="v08-slider-header">
                            <span>CPI Inflation (YoY)</span>
                            <span id="v08-val-inf" class="text-primary">2.5%</span>
                        </div>
                        <input type="range" id="v08-slide-inf" class="v08-slider" data-type="risk" min="0" max="15" step="0.1" value="2.5">
                    </div>

                    <div class="v08-slider-group" style="margin-top: var(--space-md);">
                        <div class="v08-slider-header">
                            <span>Central Bank Rate</span>
                            <span id="v08-val-int" class="text-primary">4.0%</span>
                        </div>
                        <input type="range" id="v08-slide-int" class="v08-slider" data-type="neutral" min="0" max="10" step="0.1" value="4.0">
                    </div>
                </div>

                <div>
                    <div class="kpi-label">Internal Strategic Levers</div>
                    
                    <div class="v08-slider-group" style="margin-top: var(--space-md);">
                        <div class="v08-slider-header">
                            <span>OPEX Flex / Optimization</span>
                            <span id="v08-val-opx" class="text-primary">0.0%</span>
                        </div>
                        <input type="range" id="v08-slide-opx" class="v08-slider" data-type="neutral" min="-30" max="30" step="0.5" value="0.0">
                    </div>

                    <div class="v08-slider-group" style="margin-top: var(--space-md);">
                        <div class="v08-slider-header">
                            <span>Sales Vol. Growth Target</span>
                            <span id="v08-val-grw" class="text-primary">+5.0%</span>
                        </div>
                        <input type="range" id="v08-slide-grw" class="v08-slider" data-type="growth" min="-15" max="35" step="0.5" value="5.0">
                    </div>
                </div>
            </div>

            <div class="v08-output-area">
                
                <div class="v08-scenario-header">
                    <div class="kpi-label">Active Simulation Profile</div>
                    <h3 id="v08-scen-title" style="font-size: 2rem; color: var(--text-primary); margin-bottom: 0.5rem; transition: color 0.3s;">Current Baseline Vector</h3>
                    <div id="v08-scen-insight" class="font-mono text-accent" style="font-size: 0.85rem;">
                        > DS_LOG: Modell operiert auf aktuellen Marktdaten. Keine Anomalien induziert.
                    </div>
                </div>

                <div class="v08-gauge-card">
                    <svg class="v08-gauge-svg">
                        <circle class="v08-gauge-bg" cx="90" cy="90" r="70" />
                        <circle id="v08-fill-fcf" class="v08-gauge-fill" cx="90" cy="90" r="70" />
                    </svg>
                    <div class="v08-gauge-content">
                        <div class="v08-gauge-value" id="v08-val-fcf">€142.5M</div>
                        <div class="v08-gauge-label">Predictive FCF</div>
                        <div class="v08-delta-badge" id="v08-delta-fcf">0.0% vs Base</div>
                    </div>
                </div>

                <div class="v08-gauge-card">
                    <svg class="v08-gauge-svg">
                        <circle class="v08-gauge-bg" cx="90" cy="90" r="70" />
                        <circle id="v08-fill-val" class="v08-gauge-fill" cx="90" cy="90" r="70" />
                    </svg>
                    <div class="v08-gauge-content">
                        <div class="v08-gauge-value" id="v08-val-val">€1.25B</div>
                        <div class="v08-gauge-label">DCF Valuation</div>
                        <div class="v08-delta-badge" id="v08-delta-val">0.0% vs Base</div>
                    </div>
                </div>

                <div class="v08-gauge-card" style="grid-column: 1 / -1; flex-direction: row; justify-content: space-between; padding: var(--space-xl);">
                    <div>
                        <div class="kpi-label">EBITDA Margin Output</div>
                        <div class="v08-gauge-value" id="v08-val-margin" style="font-size: 3.5rem;">34.0%</div>
                        <div class="v08-delta-badge" id="v08-delta-margin" style="display: inline-block; margin-top: 12px; font-size: 0.9rem;">0.0% vs Base</div>
                    </div>
                    
                    <div style="width: 50%; height: 6px; background: rgba(255,255,255,0.05); border-radius: 3px; position: relative; overflow: hidden;">
                        <div id="v08-fill-margin" style="position: absolute; top: 0; left: 0; height: 100%; background: var(--gauge-color, var(--acc-cyan)); width: 68%; transition: width 1s var(--ease-out-expo), background 0.5s;"></div>
                    </div>
                </div>

            </div>

            <script>
                {js_inject}
            </script>
        </section>
        """.replace("{css_inject}", self.build_css()).replace("{js_inject}", self.build_js())

    def get_output(self) -> str:
        return self.build_html()

if __name__ == "__main__":
    builder = SandboxScenarioBuilder()
    html_output = builder.get_output()
    print(html_output)