# ==============================================================================
# DATEINAME: 05_working_capital_3d.py
# VIEW: 05 - Isometric Working Capital Dynamics & Anomaly Detection
# ==============================================================================
"""
Dieses Skript generiert die fünfte Ansichtsseite (View 05).
Es implementiert eine echte 3D-CSS (Isometrische) Visualisierung des Working Capitals
(Accounts Receivable, Accounts Payable, Inventory) aufgebrochen in Aging-Buckets (0-30, 31-60, etc.).
Die Pfeiltasten LINKS/RECHTS rotieren den Fokus zwischen den Kapitalbindungsarten.
Data Science Fokus: Anomalie-Erkennung bei überfälligen Zahlungen (DSO Spikes).
"""

import json

class IsometricWorkingCapitalBuilder:
    def __init__(self):
        self.view_id = "view-05"
        
        # High-End Data Payload für Aging Buckets (Werte repräsentieren Höhe in %, Max 100)
        self.wc_data = {
            "AR": {
                "title": "Accounts Receivable (DSO)",
                "metric": "€184.2M",
                "status": "High Risk",
                "color": "var(--acc-amber)",
                "insight": "Anomaly Detected: K-Means Cluster zeigt unnatürliche Häufung im >90 Tage Bucket (Client Segment C).",
                "buckets": [
                    {"label": "0-30d", "h": 70, "val": "€60M", "alert": False},
                    {"label": "31-60d", "h": 45, "val": "€35M", "alert": False},
                    {"label": "61-90d", "h": 25, "val": "€15M", "alert": False},
                    {"label": ">90d", "h": 85, "val": "€74.2M", "alert": True} # Anomaly Spike
                ]
            },
            "AP": {
                "title": "Accounts Payable (DPO)",
                "metric": "€142.5M",
                "status": "Healthy",
                "color": "var(--acc-cyan)",
                "insight": "Zahlungsziele optimal ausgenutzt. Keine Skonto-Verluste identifiziert.",
                "buckets": [
                    {"label": "0-30d", "h": 90, "val": "€80M", "alert": False},
                    {"label": "31-60d", "h": 60, "val": "€45M", "alert": False},
                    {"label": "61-90d", "h": 20, "val": "€12M", "alert": False},
                    {"label": ">90d", "h": 10, "val": "€5.5M", "alert": False}
                ]
            },
            "INV": {
                "title": "Inventory Turnover (DIO)",
                "metric": "€95.8M",
                "status": "Optimized",
                "color": "var(--acc-purple)",
                "insight": "JIT-Lieferkette stabil. Leichter Überhang in Region EMEA durch Puffer-Strategie.",
                "buckets": [
                    {"label": "Fast", "h": 80, "val": "€65M", "alert": False},
                    {"label": "Mid", "h": 40, "val": "€22M", "alert": False},
                    {"label": "Slow", "h": 15, "val": "€6.8M", "alert": False},
                    {"label": "Dead", "h": 5, "val": "€2M", "alert": False}
                ]
            }
        }

    def build_css(self) -> str:
        """CSS für CSS3D Isometric Transforms und animierte Volumetrie."""
        return """
        /* ==========================================================================
           VIEW 05: ISOMETRIC 3D WORKING CAPITAL STYLES
           ========================================================================== */
        #view-05 {
            display: grid;
            grid-template-columns: 350px 1fr;
            grid-gap: var(--space-xl);
            align-items: center;
        }

        .v05-sidebar {
            display: flex;
            flex-direction: column;
            gap: var(--space-md);
            z-index: 2;
        }

        /* 3D Scene Setup */
        .v05-scene {
            width: 100%;
            height: 70vh;
            perspective: 1200px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            border-radius: 8px;
            background: radial-gradient(circle at center, var(--bg-surface-elevated) 0%, transparent 70%);
        }

        /* The Isometric Floor */
        .v05-floor {
            position: relative;
            width: 400px;
            height: 400px;
            transform-style: preserve-3d;
            transform: rotateX(60deg) rotateZ(-45deg);
            transition: transform var(--duration-slow) var(--ease-out-expo);
            /* Grid floor texture */
            background-image: 
                linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px);
            background-size: 50px 50px;
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 0 50px rgba(0,0,0,0.8);
        }

        /* 3D Bars */
        .v05-bar-group {
            position: absolute;
            transform-style: preserve-3d;
            width: 40px;
            height: 40px;
            bottom: 50px;
            transition: transform var(--duration-medium) var(--ease-out-expo);
        }

        /* Placements on the floor grid */
        .v05-bar-group:nth-child(1) { left: 50px; }
        .v05-bar-group:nth-child(2) { left: 150px; }
        .v05-bar-group:nth-child(3) { left: 250px; }
        .v05-bar-group:nth-child(4) { left: 350px; }

        /* The Bar Volume */
        .v05-bar {
            position: absolute;
            width: 100%;
            height: 100%;
            transform-style: preserve-3d;
            /* Height is controlled via JS CSS variables */
            transform: translateZ(var(--bar-h, 0px));
            transition: transform 0.8s var(--ease-out-expo),
                        background 0.8s;
        }

        /* Top Face */
        .v05-bar-face-top {
            position: absolute;
            width: 40px;
            height: 40px;
            background: var(--bar-color, var(--acc-cyan));
            border: 1px solid rgba(255,255,255,0.2);
            opacity: 0.9;
        }

        /* Left Face (Depth) */
        .v05-bar-face-left {
            position: absolute;
            width: 40px;
            height: var(--bar-h, 0px);
            background: var(--bar-color, var(--acc-cyan));
            transform-origin: top left;
            transform: rotateX(-90deg) rotateY(-90deg) translateZ(40px);
            border: 1px solid rgba(255,255,255,0.1);
            filter: brightness(0.6);
            transition: height 0.8s var(--ease-out-expo);
        }

        /* Right Face (Depth) */
        .v05-bar-face-right {
            position: absolute;
            width: 40px;
            height: var(--bar-h, 0px);
            background: var(--bar-color, var(--acc-cyan));
            transform-origin: top left;
            transform: rotateX(-90deg);
            border: 1px solid rgba(255,255,255,0.1);
            filter: brightness(0.4);
            transition: height 0.8s var(--ease-out-expo);
        }

        /* Anomaly Pulse Effect */
        .v05-bar.is-alert .v05-bar-face-top {
            box-shadow: 0 0 20px var(--acc-amber), inset 0 0 10px #fff;
            animation: pulseAlert 1.5s infinite alternate;
        }

        @keyframes pulseAlert {
            0% { filter: brightness(1); }
            100% { filter: brightness(1.5); }
        }

        /* Floor Labels */
        .v05-floor-label {
            position: absolute;
            bottom: -30px;
            left: 0;
            width: 40px;
            text-align: center;
            transform: rotateZ(90deg) rotateX(-90deg) translateY(-20px);
            font-family: var(--font-mono);
            font-size: 14px;
            color: var(--text-secondary);
            pointer-events: none;
        }

        /* Nav Pills */
        .v05-nav-pills {
            display: flex;
            gap: var(--space-sm);
            background: rgba(255,255,255,0.02);
            padding: 4px;
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.05);
        }
        
        .v05-pill {
            flex: 1;
            text-align: center;
            padding: 6px 12px;
            border-radius: 16px;
            font-size: 0.75rem;
            font-family: var(--font-mono);
            color: var(--text-tertiary);
            cursor: pointer;
            transition: all var(--duration-fast);
        }
        
        .v05-pill.is-active {
            background: var(--bg-surface-elevated);
            color: var(--text-primary);
            box-shadow: 0 2px 8px rgba(0,0,0,0.5);
        }
        """

    def build_js(self) -> str:
        """Controller für View 05: 3D Data Mapping und State Transitions."""
        return f"""
        /* ==========================================================================
           VIEW 05 CONTROLLER: 3D ISOMETRIC ENGINE
           ========================================================================== */
        class View05Controller {{
            constructor() {{
                this.viewElement = document.getElementById('{self.view_id}');
                this.wcKeys = ['AR', 'AP', 'INV'];
                this.wcData = {json.dumps(self.wcData)};
                this.currentIndex = 0;
                
                this.initEvents();
            }}

            initEvents() {{
                window.addEventListener('keydown', (e) => {{
                    if (!this.viewElement || !this.viewElement.classList.contains('is-active')) return;

                    if (e.key === 'ArrowRight') {{
                        e.stopPropagation();
                        this.switchDataset(1);
                    }} else if (e.key === 'ArrowLeft') {{
                        e.stopPropagation();
                        this.switchDataset(-1);
                    }}
                }}, true);
            }}

            switchDataset(direction) {{
                this.currentIndex += direction;
                if (this.currentIndex >= this.wcKeys.length) this.currentIndex = 0;
                if (this.currentIndex < 0) this.currentIndex = this.wcKeys.length - 1;
                
                this.renderState();
            }}

            renderState() {{
                const key = this.wcKeys[this.currentIndex];
                const data = this.wcData[key];

                // Update Sidebar UI
                document.getElementById('v05-title').innerText = data.title;
                document.getElementById('v05-metric').innerText = data.metric;
                document.getElementById('v05-metric').style.color = data.color;
                
                const statusEl = document.getElementById('v05-status');
                statusEl.innerText = data.status;
                statusEl.style.color = data.status === 'High Risk' ? 'var(--acc-amber)' : 'var(--acc-green)';
                
                document.getElementById('v05-insight').innerText = '> ' + data.insight;

                // Update Pills
                document.querySelectorAll('.v05-pill').forEach((pill, idx) => {{
                    pill.classList.toggle('is-active', idx === this.currentIndex);
                }});

                // Update 3D Bars via CSS Variables
                const barGroups = document.querySelectorAll('.v05-bar-group');
                
                data.buckets.forEach((bucket, i) => {{
                    if(barGroups[i]) {{
                        const bar = barGroups[i].querySelector('.v05-bar');
                        const label = barGroups[i].querySelector('.v05-floor-label');
                        const valueLabel = document.getElementById(`v05-val-${{i}}`);
                        
                        // Map 0-100 to 0-250px height
                        const pxHeight = (bucket.h / 100) * 250;
                        
                        // Apply CSS variables to trigger native transitions
                        bar.style.setProperty('--bar-h', `${{pxHeight}}px`);
                        bar.style.setProperty('--bar-color', data.color);
                        
                        // Anomaly styling
                        if (bucket.alert) {{
                            bar.classList.add('is-alert');
                            bar.style.setProperty('--bar-color', 'var(--acc-amber)');
                        }} else {{
                            bar.classList.remove('is-alert');
                        }}
                        
                        // Text updates
                        if(label) label.innerText = bucket.label;
                        if(valueLabel) {{
                            valueLabel.innerText = bucket.val;
                            valueLabel.style.color = bucket.alert ? 'var(--acc-amber)' : 'var(--text-primary)';
                        }}
                    }}
                }});

                // Subtle floor rotation for dynamic feeling
                const floor = document.querySelector('.v05-floor');
                const rotation = -45 + (this.currentIndex * 10); // Shifts angle slightly
                floor.style.transform = `rotateX(60deg) rotateZ(${{rotation}}deg)`;
            }}
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            window.V05Controller = new View05Controller();
            setTimeout(() => window.V05Controller.renderState(), 1200);
        }});
        """

    @property
    def wcData(self):
        return self.wc_data

    def build_html(self) -> str:
        """Generiert das HTML für View 05."""
        return """
        <section class="view-container" id="view-05">
            
            <style>
                {css_inject}
            </style>

            <div class="v05-sidebar">
                <div class="v05-nav-pills">
                    <div class="v05-pill is-active">AR Aging</div>
                    <div class="v05-pill">AP Aging</div>
                    <div class="v05-pill">Inventory</div>
                </div>

                <div style="margin-top: var(--space-md);">
                    <h2 id="v05-title" style="font-size: 1.8rem; font-weight: 300; margin-bottom: 0.25rem;">
                        Accounts Receivable (DSO)
                    </h2>
                    <div class="font-mono text-secondary" style="font-size: 0.8rem; margin-bottom: var(--space-md);">
                        System Status: <span id="v05-status" style="color: var(--acc-amber);">High Risk</span>
                    </div>
                </div>

                <div class="kpi-card" style="border-left: 2px solid var(--acc-cyan);">
                    <div class="kpi-label">Total Volume Bound</div>
                    <div class="kpi-value" id="v05-metric" style="color: var(--acc-amber); font-size: 2.5rem;">€184.2M</div>
                    <div id="v05-insight" class="text-secondary font-mono" style="font-size: 0.8rem; margin-top: var(--space-sm); border-top: 1px solid rgba(255,255,255,0.1); padding-top: var(--space-sm);">
                        > Anomaly Detected: K-Means Cluster zeigt unnatürliche Häufung im >90 Tage Bucket (Client Segment C).
                    </div>
                </div>

                <div class="kpi-card" style="padding: var(--space-sm) var(--space-md);">
                    <table style="width: 100%; text-align: left; font-family: var(--font-mono); font-size: 0.85rem; border-collapse: collapse;">
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                            <td style="padding: 8px 0; color: var(--text-tertiary);">Bucket 1</td>
                            <td id="v05-val-0" style="text-align: right;">--</td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                            <td style="padding: 8px 0; color: var(--text-tertiary);">Bucket 2</td>
                            <td id="v05-val-1" style="text-align: right;">--</td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                            <td style="padding: 8px 0; color: var(--text-tertiary);">Bucket 3</td>
                            <td id="v05-val-2" style="text-align: right;">--</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: var(--text-tertiary);">Bucket 4</td>
                            <td id="v05-val-3" style="text-align: right; font-weight: bold;">--</td>
                        </tr>
                    </table>
                </div>
            </div>

            <div class="v05-scene">
                <div class="v05-floor">
                    
                    <div class="v05-bar-group">
                        <div class="v05-bar">
                            <div class="v05-bar-face-top"></div>
                            <div class="v05-bar-face-left"></div>
                            <div class="v05-bar-face-right"></div>
                        </div>
                        <div class="v05-floor-label">0-30d</div>
                    </div>

                    <div class="v05-bar-group">
                        <div class="v05-bar">
                            <div class="v05-bar-face-top"></div>
                            <div class="v05-bar-face-left"></div>
                            <div class="v05-bar-face-right"></div>
                        </div>
                        <div class="v05-floor-label">31-60d</div>
                    </div>

                    <div class="v05-bar-group">
                        <div class="v05-bar">
                            <div class="v05-bar-face-top"></div>
                            <div class="v05-bar-face-left"></div>
                            <div class="v05-bar-face-right"></div>
                        </div>
                        <div class="v05-floor-label">61-90d</div>
                    </div>

                    <div class="v05-bar-group">
                        <div class="v05-bar">
                            <div class="v05-bar-face-top"></div>
                            <div class="v05-bar-face-left"></div>
                            <div class="v05-bar-face-right"></div>
                        </div>
                        <div class="v05-floor-label">>90d</div>
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
    builder = IsometricWorkingCapitalBuilder()
    html_output = builder.get_output()
    print(html_output)