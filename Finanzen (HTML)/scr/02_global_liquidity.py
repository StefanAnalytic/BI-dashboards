# ==============================================================================
# DATEINAME: 02_global_liquidity.py
# VIEW: 02 - Real-Time Liquidity Map & Currency Exposure
# ==============================================================================
"""
Dieses Skript generiert exklusiv die zweite Ansichtsseite (View 02).
Es implementiert eine interaktive, knotenbasierte Liquiditätskarte mit Sub-Navigation.
Die Pfeiltasten LINKS/RECHTS iterieren innerhalb dieser View durch Währungsräume
(USD, EUR, APAC), während HOCH/RUNTER (durch die globale Engine) die View wechseln.
"""

import json

class LiquidityMapBuilder:
    def __init__(self):
        self.view_id = "view-02"
        # High-End Data Payload (Mocked for Presentation)
        self.currency_zones = {
            "USD": {"liquidity": "84.2M", "risk": "Low", "trend": "+2.1%", "nodes": [{"x": 20, "y": 40, "label": "NY", "size": 1.5}, {"x": 15, "y": 45, "label": "CHI", "size": 0.8}]},
            "EUR": {"liquidity": "42.8M", "risk": "Medium", "trend": "-1.4%", "nodes": [{"x": 48, "y": 35, "label": "FRA", "size": 1.2}, {"x": 45, "y": 33, "label": "LDN", "size": 1.6}]},
            "APAC": {"liquidity": "56.0M", "risk": "High", "trend": "+5.8%", "nodes": [{"x": 80, "y": 45, "label": "SGP", "size": 1.4}, {"x": 85, "y": 38, "label": "TYO", "size": 1.8}]}
        }

    def build_css(self) -> str:
        """Spezifisches CSS für die Liquiditätskarte und Node-Animationen."""
        return """
        /* ==========================================================================
           VIEW 02: LIQUIDITY MAP STYLES
           ========================================================================== */
        #view-02 {
            /* Überschreibt das Standard-Grid für ein raumfüllendes Map-Layout */
            display: grid;
            grid-template-columns: 350px 1fr;
            grid-template-rows: 1fr;
            gap: var(--space-xl);
            align-items: center;
        }

        .v02-sidebar {
            display: flex;
            flex-direction: column;
            gap: var(--space-md);
            height: 100%;
            justify-content: center;
            position: relative;
            z-index: 2;
        }

        .v02-map-container {
            position: relative;
            width: 100%;
            height: 80vh;
            background: radial-gradient(circle at center, var(--bg-surface-elevated) 0%, transparent 70%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* Sub-Navigation Indicators (Left/Right) */
        .v02-zone-selector {
            display: flex;
            gap: var(--space-sm);
            margin-bottom: var(--space-md);
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: var(--space-sm);
        }

        .v02-zone-btn {
            background: none;
            border: none;
            color: var(--text-tertiary);
            font-family: var(--font-mono);
            font-size: 0.85rem;
            cursor: pointer;
            transition: color var(--duration-fast), text-shadow var(--duration-fast);
            position: relative;
        }

        .v02-zone-btn.is-active {
            color: var(--acc-cyan);
            text-shadow: 0 0 8px var(--acc-cyan-glow);
        }

        .v02-zone-btn.is-active::after {
            content: '';
            position: absolute;
            bottom: -calc(var(--space-sm) + 1px);
            left: 0;
            width: 100%;
            height: 2px;
            background: var(--acc-cyan);
            box-shadow: 0 0 10px var(--acc-cyan);
        }

        /* Abstract Node Map SVGs */
        .v02-node {
            fill: var(--text-secondary);
            transition: fill var(--duration-medium), r var(--duration-medium);
            cursor: crosshair;
        }
        
        .v02-node.is-active-zone {
            fill: var(--acc-cyan);
            filter: drop-shadow(0 0 6px var(--acc-cyan));
            animation: nodePulse 2s infinite var(--ease-in-out-circ);
        }

        .v02-connection {
            stroke: rgba(255,255,255,0.05);
            stroke-width: 0.5;
            fill: none;
            transition: stroke var(--duration-medium);
        }

        .v02-connection.is-active-zone {
            stroke: var(--acc-cyan);
            stroke-opacity: 0.4;
            stroke-dasharray: 4;
            animation: flowDash 20s linear infinite;
        }

        @keyframes nodePulse {
            0% { transform: scale(1); opacity: 0.8; }
            50% { transform: scale(1.3); opacity: 1; }
            100% { transform: scale(1); opacity: 0.8; }
        }

        @keyframes flowDash {
            to { stroke-dashoffset: -100; }
        }

        /* Detail Panel Transition */
        .v02-detail-panel {
            opacity: 0;
            transform: translateX(-20px);
            transition: all var(--duration-medium) var(--ease-out-expo);
        }
        .v02-detail-panel.is-visible {
            opacity: 1;
            transform: translateX(0);
        }
        """

    def build_js(self) -> str:
        """Isolierter Controller für View 02 (Sub-State Management)."""
        return f"""
        /* ==========================================================================
           VIEW 02 CONTROLLER: LATERAL NAVIGATION & DATA BINDING
           ========================================================================== */
        class View02Controller {{
            constructor() {{
                this.viewElement = document.getElementById('{self.view_id}');
                this.zones = {json.dumps(list(self.currency_zones.keys()))};
                this.zoneData = {json.dumps(self.currency_zones)};
                this.currentIndex = 0;
                
                this.initEvents();
            }}

            initEvents() {{
                // Intercept Keyboard specifically for this View when active
                window.addEventListener('keydown', (e) => {{
                    if (!this.viewElement || !this.viewElement.classList.contains('is-active')) return;

                    // Override Left/Right for internal state
                    if (e.key === 'ArrowRight') {{
                        e.stopPropagation(); // Prevent global engine from switching view
                        this.switchZone(1);
                    }} else if (e.key === 'ArrowLeft') {{
                        e.stopPropagation();
                        this.switchZone(-1);
                    }}
                }}, true); // Use capture phase to intercept before global engine
            }}

            switchZone(direction) {{
                this.currentIndex += direction;
                if (this.currentIndex >= this.zones.length) this.currentIndex = 0;
                if (this.currentIndex < 0) this.currentIndex = this.zones.length - 1;
                
                this.renderState();
            }}

            renderState() {{
                const activeZone = this.zones[this.currentIndex];
                const data = this.zoneData[activeZone];

                // Update UI Buttons
                document.querySelectorAll('.v02-zone-btn').forEach((btn, idx) => {{
                    btn.classList.toggle('is-active', idx === this.currentIndex);
                }});

                // Update Metrics with Animation trigger
                const panel = document.querySelector('.v02-detail-panel');
                panel.classList.remove('is-visible');
                
                setTimeout(() => {{
                    document.getElementById('v02-val-liquidity').innerText = data.liquidity;
                    document.getElementById('v02-val-risk').innerText = data.risk;
                    document.getElementById('v02-val-trend').innerText = data.trend;
                    
                    // Specific coloring based on risk
                    const riskEl = document.getElementById('v02-val-risk');
                    riskEl.style.color = data.risk === 'High' ? 'var(--acc-red)' : 
                                         data.risk === 'Medium' ? 'var(--acc-amber)' : 'var(--acc-green)';

                    panel.classList.add('is-visible');
                }}, 50); // Micro-delay to re-trigger CSS transition

                // Update SVG Map Nodes
                document.querySelectorAll('.v02-node').forEach(node => {{
                    if (node.dataset.zone === activeZone) {{
                        node.classList.add('is-active-zone');
                    }} else {{
                        node.classList.remove('is-active-zone');
                    }}
                }});

                document.querySelectorAll('.v02-connection').forEach(conn => {{
                    if (conn.dataset.zone === activeZone) {{
                        conn.classList.add('is-active-zone');
                    }} else {{
                        conn.classList.remove('is-active-zone');
                    }}
                }});
            }}
        }}

        // Initialize Controller when document is ready
        document.addEventListener('DOMContentLoaded', () => {{
            window.V02Controller = new View02Controller();
            // Initial render
            setTimeout(() => window.V02Controller.renderState(), 500);
        }});
        """

    def build_html(self) -> str:
        """Generiert das HTML für View 02 inkl. SVG Abstract Map."""
        return """
        <section class="view-container" id="view-02">
            
            <style>
                {css_inject}
            </style>

            <div class="v02-sidebar">
                <div>
                    <h2 style="font-size: 2rem; font-weight: 300; margin-bottom: 0.5rem;">
                        Global Liquidity <span class="font-mono text-accent">Topology</span>
                    </h2>
                    <p class="text-secondary" style="font-size: 0.9rem;">
                        Echtzeit-Kapitalbindung aggregiert nach juristischen Entitäten und Währungsräumen. 
                        Navigation via <kbd class="font-mono text-primary" style="background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">&larr;</kbd> <kbd class="font-mono text-primary" style="background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">&rarr;</kbd> Tasten.
                    </p>
                </div>

                <div class="v02-zone-selector">
                    <button class="v02-zone-btn is-active">USD Zone</button>
                    <button class="v02-zone-btn">EUR Zone</button>
                    <button class="v02-zone-btn">APAC Zone</button>
                </div>

                <div class="v02-detail-panel is-visible kpi-card">
                    <div style="margin-bottom: var(--space-md);">
                        <div class="kpi-label">Available Liquidity</div>
                        <div class="kpi-value"><span style="font-size:1.5rem; color:var(--text-tertiary)">€</span><span id="v02-val-liquidity">84.2M</span></div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-sm);">
                        <div>
                            <div class="kpi-label">FX Risk Exposure</div>
                            <div class="font-mono" id="v02-val-risk" style="font-size: 1.25rem; color: var(--acc-green);">Low</div>
                        </div>
                        <div>
                            <div class="kpi-label">30-Day Trend</div>
                            <div class="font-mono" id="v02-val-trend" style="font-size: 1.25rem; color: var(--text-primary);">+2.1%</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="v02-map-container">
                <svg width="100%" height="100%" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid slice">
                    <pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">
                        <path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.02)" stroke-width="0.5"/>
                    </pattern>
                    <rect width="100" height="100" fill="url(#grid)" />

                    <path class="v02-connection is-active-zone" data-zone="USD" d="M20,40 Q35,30 50,50" />
                    <path class="v02-connection is-active-zone" data-zone="USD" d="M15,45 Q20,60 50,50" />
                    
                    <path class="v02-connection" data-zone="EUR" d="M48,35 Q50,45 50,50" />
                    <path class="v02-connection" data-zone="EUR" d="M45,33 Q60,20 80,45" />

                    <path class="v02-connection" data-zone="APAC" d="M80,45 Q65,60 50,50" />
                    <path class="v02-connection" data-zone="APAC" d="M85,38 Q95,50 80,45" />

                    <circle cx="50" cy="50" r="3" fill="none" stroke="var(--text-tertiary)" stroke-width="0.5" />
                    <circle cx="50" cy="50" r="1" fill="var(--text-primary)" />

                    <circle class="v02-node is-active-zone" data-zone="USD" cx="20" cy="40" r="1.5" />
                    <text x="20" y="37" font-size="2" fill="var(--text-tertiary)" class="font-mono" text-anchor="middle">NY</text>
                    
                    <circle class="v02-node is-active-zone" data-zone="USD" cx="15" cy="45" r="0.8" />
                    
                    <circle class="v02-node" data-zone="EUR" cx="48" cy="35" r="1.2" />
                    <text x="48" y="32" font-size="2" fill="var(--text-tertiary)" class="font-mono" text-anchor="middle">FRA</text>
                    
                    <circle class="v02-node" data-zone="EUR" cx="45" cy="33" r="1.6" />
                    
                    <circle class="v02-node" data-zone="APAC" cx="80" cy="45" r="1.4" />
                    <text x="80" y="42" font-size="2" fill="var(--text-tertiary)" class="font-mono" text-anchor="middle">SGP</text>
                    
                    <circle class="v02-node" data-zone="APAC" cx="85" cy="38" r="1.8" />
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
    # Instanziierung und Output-Generierung
    builder = LiquidityMapBuilder()
    html_output = builder.get_output()
    
    # Im finalen Build-Skript (Iteration 11) wird das Ergebnis von get_output() 
    # direkt in den <div id="app-root"> des Hauptdokuments injiziert.
    print(html_output)