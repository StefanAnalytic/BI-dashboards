# ==============================================================================
# DATEINAME: 07_segment_performance.py
# VIEW: 07 - Deep Dive: Segment & Product Profitability
# ==============================================================================
"""
Dieses Skript generiert die siebte Ansichtsseite (View 07).
Es implementiert eine interaktive, datengetriebene Bubble-Matrix (Scatter-Plot),
die Geschäftseinheiten nach Profitabilität (Y-Achse) und Marktwachstum (X-Achse) anordnet.
Die Pfeiltasten LINKS/RECHTS wechseln die Cluster-Dimension (Region vs. Produktlinie).
Dabei greift eine "Vanilla JS Physics Engine", die die Bubbles flüssig an ihre 
neuen Koordinaten morpht (ähnlich D3.js, aber komplett nativ für maximale Performance).
Data Science Fokus: Gaussian Mixture Models (GMM) für multidimensionales Clustering.
"""

import json

class SegmentPerformanceBuilder:
    def __init__(self):
        self.view_id = "view-07"
        
        # High-End Data Payload: Multi-Dimensional Clusters
        # x = Growth (0-100 mapped to SVG), y = Margin (0-100, inverted for SVG), r = Volume
        self.cluster_datasets = {
            "Region": {
                "title": "Geospatial Profitability Clustering",
                "insight": "GMM (Gaussian Mixture Model) identifiziert APAC als High-Growth/High-Margin 'Star' Cluster. EMEA kämpft mit CAC-Eskalation.",
                "nodes": [
                    {"id": "n1", "label": "APAC", "x": 80, "y": 20, "r": 45, "color": "var(--acc-cyan)", "rev": "€112M", "margin": "34%"},
                    {"id": "n2", "label": "NA", "x": 60, "y": 40, "r": 65, "color": "var(--acc-purple)", "rev": "€184M", "margin": "28%"},
                    {"id": "n3", "label": "EMEA", "x": 30, "y": 75, "r": 50, "color": "var(--acc-amber)", "rev": "€95M", "margin": "14%"},
                    {"id": "n4", "label": "LATAM", "x": 45, "y": 55, "r": 25, "color": "var(--text-secondary)", "rev": "€32M", "margin": "22%"}
                ]
            },
            "Product": {
                "title": "Product Line Margin Matrix",
                "insight": "SaaS-Produkte dominieren das obere Quartil. Hardware-Sparte zeigt negatives Momentum (Outlier Detection: Supply Chain).",
                "nodes": [
                    {"id": "n1", "label": "SaaS", "x": 85, "y": 15, "r": 70, "color": "var(--acc-cyan)", "rev": "€210M", "margin": "42%"},
                    {"id": "n2", "label": "Services", "x": 50, "y": 60, "r": 40, "color": "var(--text-secondary)", "rev": "€85M", "margin": "18%"},
                    {"id": "n3", "label": "Hardware", "x": 15, "y": 85, "r": 55, "color": "var(--acc-red)", "rev": "€105M", "margin": "8%"},
                    {"id": "n4", "label": "Data API", "x": 70, "y": 30, "r": 20, "color": "var(--acc-purple)", "rev": "€23M", "margin": "38%"}
                ]
            }
        }

    def build_css(self) -> str:
        """CSS für den Bubble-Chart, Grid-Lines und flüssige Morph-Transitions."""
        return """
        /* ==========================================================================
           VIEW 07: SEGMENT PERFORMANCE STYLES
           ========================================================================== */
        #view-07 {
            display: grid;
            grid-template-columns: 350px 1fr;
            grid-gap: var(--space-xl);
            align-items: center;
        }

        .v07-sidebar {
            display: flex;
            flex-direction: column;
            gap: var(--space-md);
            z-index: 2;
        }

        /* SVG Chart Container */
        .v07-chart-area {
            position: relative;
            width: 100%;
            height: 75vh;
            background: var(--bg-surface);
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.05);
            padding: var(--space-md);
            overflow: hidden;
            box-shadow: inset 0 0 100px rgba(0,0,0,0.5);
        }

        /* Grid Background within SVG */
        .v07-grid-line {
            stroke: rgba(255,255,255,0.03);
            stroke-width: 1;
        }
        
        .v07-axis-line {
            stroke: var(--text-tertiary);
            stroke-width: 1.5;
        }

        .v07-axis-label {
            fill: var(--text-tertiary);
            font-family: var(--font-mono);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }

        /* Chart Quadrants (Boston Consulting Group Matrix style overlay) */
        .v07-quadrant-label {
            fill: rgba(255,255,255,0.05);
            font-family: var(--font-sans);
            font-size: 3rem;
            font-weight: 600;
            text-transform: uppercase;
            pointer-events: none;
        }

        /* Data Bubbles */
        .v07-bubble-group {
            /* Smooth transitions for moving between coordinate sets */
            transition: transform 1.2s var(--ease-in-out-circ);
            cursor: crosshair;
        }

        .v07-bubble {
            fill: var(--bubble-color, var(--text-secondary));
            fill-opacity: 0.15;
            stroke: var(--bubble-color, var(--text-secondary));
            stroke-width: 2;
            transition: r 1.2s var(--ease-out-expo),
                        fill-opacity var(--duration-fast);
            /* Constant subtle floating animation */
            animation: floatBubble 4s ease-in-out infinite alternate;
        }

        .v07-bubble-group:nth-child(even) .v07-bubble {
            animation-duration: 5s;
            animation-delay: -2s;
        }

        .v07-bubble-group:hover .v07-bubble {
            fill-opacity: 0.4;
            filter: drop-shadow(0 0 15px var(--bubble-color));
        }

        .v07-bubble-label {
            fill: var(--text-primary);
            font-family: var(--font-sans);
            font-size: 14px;
            font-weight: 400;
            text-anchor: middle;
            pointer-events: none;
            text-shadow: 0 2px 4px rgba(0,0,0,0.8);
            transition: opacity var(--duration-medium);
        }

        .v07-bubble-metric {
            fill: var(--text-secondary);
            font-family: var(--font-mono);
            font-size: 11px;
            text-anchor: middle;
            pointer-events: none;
        }

        @keyframes floatBubble {
            0% { transform: translateY(-3px); }
            100% { transform: translateY(3px); }
        }

        /* Navigation Tabs */
        .v07-tabs {
            display: flex;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            margin-bottom: var(--space-md);
        }

        .v07-tab {
            padding: var(--space-sm) var(--space-md);
            color: var(--text-tertiary);
            font-family: var(--font-mono);
            font-size: 0.8rem;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            transition: all var(--duration-fast);
        }

        .v07-tab.is-active {
            color: var(--acc-cyan);
            border-bottom-color: var(--acc-cyan);
            text-shadow: 0 0 8px var(--acc-cyan-glow);
        }
        """

    def build_js(self) -> str:
        """Controller für View 07: Morphing-Logik und Daten-Bindung für SVG-Nodes."""
        return f"""
        /* ==========================================================================
           VIEW 07 CONTROLLER: SVG BUBBLE PHYSICS & CLUSTERING
           ========================================================================== */
        class View07Controller {{
            constructor() {{
                this.viewElement = document.getElementById('{self.view_id}');
                this.dimensions = ['Region', 'Product'];
                this.clusterData = {json.dumps(self.cluster_datasets)};
                this.currentIndex = 0;
                
                this.initEvents();
            }}

            initEvents() {{
                window.addEventListener('keydown', (e) => {{
                    if (!this.viewElement || !this.viewElement.classList.contains('is-active')) return;

                    if (e.key === 'ArrowRight') {{
                        e.stopPropagation();
                        this.switchDimension(1);
                    }} else if (e.key === 'ArrowLeft') {{
                        e.stopPropagation();
                        this.switchDimension(-1);
                    }}
                }}, true);
            }}

            switchDimension(direction) {{
                this.currentIndex += direction;
                if (this.currentIndex >= this.dimensions.length) this.currentIndex = 0;
                if (this.currentIndex < 0) this.currentIndex = this.dimensions.length - 1;
                
                this.renderState();
            }}

            renderState() {{
                const dimKey = this.dimensions[this.currentIndex];
                const data = this.clusterData[dimKey];

                // Update UI Texts
                document.getElementById('v07-title').innerText = data.title;
                
                const insightEl = document.getElementById('v07-insight');
                insightEl.style.opacity = 0;
                setTimeout(() => {{
                    insightEl.innerText = '> DS_LOG: ' + data.insight;
                    insightEl.style.opacity = 1;
                }}, 300);

                // Update Tabs
                document.querySelectorAll('.v07-tab').forEach((tab, idx) => {{
                    tab.classList.toggle('is-active', idx === this.currentIndex);
                }});

                // Morph SVG Bubbles
                // Das SVG ViewBox ist 1000x1000. Wir mappen x(0-100) -> 100-900, y(0-100) -> 900-100
                data.nodes.forEach((node, index) => {{
                    const group = document.getElementById(`v07-node-${{index}}`);
                    if (group) {{
                        const mapX = 100 + (node.x / 100) * 800;
                        const mapY = 100 + (node.y / 100) * 800; // y=0 is top in SVG, so low margin = high Y
                        
                        // Move Group
                        group.style.transform = `translate(${{mapX}}px, ${{mapY}}px)`;
                        
                        // Resize & Recolor Bubble
                        const circle = group.querySelector('circle');
                        circle.setAttribute('r', node.r);
                        circle.style.setProperty('--bubble-color', node.color);
                        
                        // Update Labels
                        const titleText = group.querySelector('.v07-bubble-label');
                        const metricText = group.querySelector('.v07-bubble-metric');
                        
                        titleText.textContent = node.label;
                        metricText.textContent = `${{node.margin}} Margin | ${{node.rev}}`;
                        
                        // Dynamic text color matching bubble
                        titleText.style.fill = node.color;
                    }}
                }});
            }}
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            window.V07Controller = new View07Controller();
            setTimeout(() => window.V07Controller.renderState(), 1600);
        }});
        """

    def build_html(self) -> str:
        """Generiert das HTML für View 07 inklusive SVG-Struktur für Scatter-Plot."""
        return """
        <section class="view-container" id="view-07">
            
            <style>
                {css_inject}
            </style>

            <div class="v07-sidebar">
                <div class="v07-tabs">
                    <div class="v07-tab is-active">Geospatial (Region)</div>
                    <div class="v07-tab">Product Line</div>
                </div>

                <div style="margin-top: var(--space-sm);">
                    <h2 id="v07-title" style="font-size: 2rem; font-weight: 300; margin-bottom: 0.5rem; line-height: 1.1;">
                        Geospatial Profitability Clustering
                    </h2>
                    <p class="text-secondary" style="font-size: 0.9rem;">
                        Identifikation von Performance-Clustern basierend auf Profitabilität (Y-Achse) und Marktwachstum (X-Achse). Kreisgröße = Umsatzvolumen.
                        <br><br>Wechsel der Daten-Dimension mit <kbd class="font-mono text-primary" style="background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">&larr;</kbd> <kbd class="font-mono text-primary" style="background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">&rarr;</kbd>.
                    </p>
                </div>

                <div class="kpi-card" style="margin-top: var(--space-md); border-top: 2px solid var(--acc-purple);">
                    <div class="kpi-label">Algorithm Insight (GMM)</div>
                    <div id="v07-insight" class="font-mono text-primary" style="font-size: 0.85rem; line-height: 1.6; transition: opacity 0.3s;">
                        > DS_LOG: GMM (Gaussian Mixture Model) identifiziert APAC als High-Growth/High-Margin 'Star' Cluster. EMEA kämpft mit CAC-Eskalation.
                    </div>
                </div>
                
                <div class="kpi-card" style="margin-top: var(--space-sm); padding: var(--space-sm) var(--space-md);">
                    <table style="width: 100%; font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-secondary);">
                        <tr>
                            <td><span style="display:inline-block; width:10px; height:10px; background:var(--acc-cyan); border-radius:50%; margin-right:5px;"></span> High Growth / Margin</td>
                            <td style="text-align: right;">Target Vector</td>
                        </tr>
                        <tr>
                            <td><span style="display:inline-block; width:10px; height:10px; background:var(--acc-amber); border-radius:50%; margin-right:5px;"></span> Margin Compression</td>
                            <td style="text-align: right;">Warning</td>
                        </tr>
                        <tr>
                            <td><span style="display:inline-block; width:10px; height:10px; background:var(--acc-red); border-radius:50%; margin-right:5px;"></span> Value Detractor</td>
                            <td style="text-align: right;">Critical</td>
                        </tr>
                    </table>
                </div>
            </div>

            <div class="v07-chart-area">
                <svg width="100%" height="100%" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid slice">
                    
                    <line class="v07-grid-line" x1="100" y1="300" x2="900" y2="300" />
                    <line class="v07-grid-line" x1="100" y1="500" x2="900" y2="500" />
                    <line class="v07-grid-line" x1="100" y1="700" x2="900" y2="700" />
                    <line class="v07-grid-line" x1="300" y1="100" x2="300" y2="900" />
                    <line class="v07-grid-line" x1="500" y1="100" x2="500" y2="900" />
                    <line class="v07-grid-line" x1="700" y1="100" x2="700" y2="900" />

                    <line class="v07-axis-line" x1="100" y1="900" x2="100" y2="100" />
                    <text class="v07-axis-label" x="80" y="500" transform="rotate(-90, 80, 500)" text-anchor="middle">Profitability (Margin %)</text>
                    
                    <line class="v07-axis-line" x1="100" y1="900" x2="900" y2="900" />
                    <text class="v07-axis-label" x="500" y="940" text-anchor="middle">Market Growth (YoY %)</text>

                    <text class="v07-quadrant-label" x="700" y="250" text-anchor="middle">STARS</text>
                    <text class="v07-quadrant-label" x="300" y="250" text-anchor="middle">QUESTIONS</text>
                    <text class="v07-quadrant-label" x="700" y="750" text-anchor="middle">CASH COWS</text>
                    <text class="v07-quadrant-label" x="300" y="750" text-anchor="middle">DOGS</text>

                    <g id="v07-node-0" class="v07-bubble-group" transform="translate(500, 500)">
                        <circle class="v07-bubble" cx="0" cy="0" r="10" />
                        <text class="v07-bubble-label" x="0" y="5">Label</text>
                        <text class="v07-bubble-metric" x="0" y="25">Metric</text>
                    </g>
                    <g id="v07-node-1" class="v07-bubble-group" transform="translate(500, 500)">
                        <circle class="v07-bubble" cx="0" cy="0" r="10" />
                        <text class="v07-bubble-label" x="0" y="5">Label</text>
                        <text class="v07-bubble-metric" x="0" y="25">Metric</text>
                    </g>
                    <g id="v07-node-2" class="v07-bubble-group" transform="translate(500, 500)">
                        <circle class="v07-bubble" cx="0" cy="0" r="10" />
                        <text class="v07-bubble-label" x="0" y="5">Label</text>
                        <text class="v07-bubble-metric" x="0" y="25">Metric</text>
                    </g>
                    <g id="v07-node-3" class="v07-bubble-group" transform="translate(500, 500)">
                        <circle class="v07-bubble" cx="0" cy="0" r="10" />
                        <text class="v07-bubble-label" x="0" y="5">Label</text>
                        <text class="v07-bubble-metric" x="0" y="25">Metric</text>
                    </g>

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
    builder = SegmentPerformanceBuilder()
    html_output = builder.get_output()
    print(html_output)