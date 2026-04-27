# ==============================================================================
# DATEINAME: 09_ai_insights_log.py
# VIEW: 09 - Generative Data Storytelling & AI Insight Feed
# ==============================================================================
"""
Dieses Skript generiert die neunte Ansichtsseite (View 09).
Es implementiert einen "Live" Data-Storytelling Feed. Hier spricht das 
finanzmathematische Modell direkt zum CFO. 
Die Pfeiltasten LINKS/RECHTS filtern den Feed nach Kategorien (Critical, Opportunity, System).
Ein Typewriter-Effekt und Staggered-Animations bei Filterwechseln sorgen für 
ein hochwertiges "Kommandozentralen"-Gefühl (Terminal Aesthetic).
"""

import json

class AIInsightsBuilder:
    def __init__(self):
        self.view_id = "view-09"
        
        # High-End Data Payload: AI Generated Insights
        self.categories = ['ALL', 'CRITICAL (VaR)', 'OPPORTUNITY (ROI)', 'SYSTEM LOGS']
        self.insights = [
            {
                "id": "log_01",
                "timestamp": "CURRENT",
                "category": "CRITICAL (VaR)",
                "severity": "high",
                "title": "Anomaly in OPEX: Marketing Spend vs CAC",
                "text": "Isolation Forest Cluster 4 zeigt eine 34%ige Entkopplung zwischen Marketingausgaben (EMEA) und Customer Acquisition Cost. Der ROI nähert sich dem Break-Even. Sofortiger Stop der Q4 Top-of-Funnel Kampagnen empfohlen.",
                "action": "Execute: Reduce EMEA MKT by 15%",
                "metric": "Risk: €4.2M"
            },
            {
                "id": "log_02",
                "timestamp": "T-04:12:00",
                "category": "OPPORTUNITY (ROI)",
                "severity": "low",
                "title": "Treasury Yield Arbitrage",
                "text": "Überflüssige Liquidität ($12.5M) im USD-Raum identifiziert. Kurzfristige US-Treasuries bieten aktuell +45bps gegenüber dem hinterlegten Baseline-Zins. Umschichtung würde das Quartalsergebnis stützen.",
                "action": "Execute: Route $12.5M to T-Bills",
                "metric": "Upside: $56k/mo"
            },
            {
                "id": "log_03",
                "timestamp": "T-18:45:22",
                "category": "CRITICAL (VaR)",
                "severity": "medium",
                "title": "Supply Chain Index (Baltic Dry) Alert",
                "text": "Vorhersagemodell (ARIMA) für Frachtkosten signalisiert einen Breakout über den 200-Tage-Durchschnitt. Historische Korrelation deutet auf Margendruck für Hardware-Sparte in T+60 Tagen hin.",
                "action": "Review: Freight Forward Contracts",
                "metric": "Impact: -1.2% Margin"
            },
            {
                "id": "log_04",
                "timestamp": "T-24:00:00",
                "category": "SYSTEM LOGS",
                "severity": "info",
                "title": "Model Recalibration Complete",
                "text": "XGBoost Probability of Default (PD) Modelle wurden mit den neuesten Rating-Agentur-Datenbanken synchronisiert. Modell-Konfidenz liegt bei 96.8%.",
                "action": "View: Model Lineage",
                "metric": "Status: Optimal"
            },
            {
                "id": "log_05",
                "timestamp": "T-36:10:05",
                "category": "OPPORTUNITY (ROI)",
                "severity": "medium",
                "title": "DSO Optimization (Accounts Receivable)",
                "text": "3 Großkunden in LATAM überziehen systematisch Zahlungsziele (Avg: 65 Tage). Implementierung eines Dynamic Discounting Programms könnte Working Capital um €3.4M entlasten.",
                "action": "Simulate: Discount Matrix",
                "metric": "Unlock: €3.4M Liquidity"
            }
        ]

    def build_css(self) -> str:
        """CSS für Terminal-Layout, Typewriter und Staggered Cards."""
        return """
        /* ==========================================================================
           VIEW 09: AI INSIGHTS LOG STYLES
           ========================================================================== */
        #view-09 {
            display: grid;
            grid-template-columns: 350px 1fr;
            grid-gap: var(--space-xl);
            align-items: start;
            padding-top: calc(var(--space-lg) * 4);
        }

        .v09-sidebar {
            display: flex;
            flex-direction: column;
            gap: var(--space-md);
            position: sticky;
            top: 20%;
        }

        /* Category Filter Tabs */
        .v09-filter-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: var(--space-sm);
            margin-top: var(--space-lg);
        }

        .v09-filter-item {
            padding: var(--space-sm) var(--space-md);
            border-left: 2px solid rgba(255,255,255,0.1);
            color: var(--text-tertiary);
            font-family: var(--font-mono);
            font-size: 0.85rem;
            cursor: pointer;
            transition: all var(--duration-fast);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .v09-filter-item.is-active {
            border-left-color: var(--acc-cyan);
            color: var(--text-primary);
            background: linear-gradient(90deg, rgba(0,240,255,0.1) 0%, transparent 100%);
        }

        .v09-filter-count {
            background: rgba(255,255,255,0.05);
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.7rem;
        }

        /* Feed Container */
        .v09-feed-container {
            display: flex;
            flex-direction: column;
            gap: var(--space-md);
            max-height: 75vh;
            overflow: hidden; /* We handle this via custom logic, no native scrollbars */
            position: relative;
            padding-right: var(--space-sm);
        }

        /* Insight Cards */
        .v09-card {
            background: var(--bg-surface);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 8px;
            padding: var(--space-lg);
            position: relative;
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.5s var(--ease-out-expo), transform 0.5s var(--ease-out-expo);
            display: none; /* Handled by JS */
        }

        .v09-card.is-visible {
            display: block;
        }

        .v09-card.is-animating {
            opacity: 1;
            transform: translateY(0);
        }

        /* Severity styling on cards */
        .v09-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; bottom: 0; width: 3px;
            border-radius: 8px 0 0 8px;
        }
        
        .v09-card[data-severity="high"]::before { background: var(--acc-red); box-shadow: 0 0 10px rgba(255, 51, 102, 0.5); }
        .v09-card[data-severity="medium"]::before { background: var(--acc-amber); }
        .v09-card[data-severity="low"]::before { background: var(--acc-cyan); }
        .v09-card[data-severity="info"]::before { background: var(--text-tertiary); }

        .v09-card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: var(--space-md);
            font-family: var(--font-mono);
            font-size: 0.75rem;
        }

        .v09-timestamp { color: var(--text-tertiary); }
        .v09-category-tag { color: var(--acc-cyan); text-transform: uppercase; }

        .v09-card-title {
            font-size: 1.25rem;
            font-weight: 400;
            margin-bottom: var(--space-sm);
            color: var(--text-primary);
        }

        .v09-card-body {
            color: var(--text-secondary);
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: var(--space-md);
        }

        .v09-card-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px dashed rgba(255,255,255,0.1);
            padding-top: var(--space-md);
        }

        .v09-btn-action {
            background: transparent;
            border: 1px solid var(--acc-cyan);
            color: var(--acc-cyan);
            padding: 6px 12px;
            border-radius: 4px;
            font-family: var(--font-mono);
            font-size: 0.75rem;
            cursor: pointer;
            transition: all var(--duration-fast);
        }

        .v09-btn-action:hover {
            background: rgba(0, 240, 255, 0.1);
            box-shadow: 0 0 8px rgba(0, 240, 255, 0.2);
        }
        
        .v09-card[data-severity="high"] .v09-btn-action { border-color: var(--acc-red); color: var(--acc-red); }
        .v09-card[data-severity="high"] .v09-btn-action:hover { background: rgba(255, 51, 102, 0.1); box-shadow: 0 0 8px rgba(255, 51, 102, 0.2); }

        .v09-metric-highlight {
            font-family: var(--font-mono);
            font-size: 1rem;
            color: var(--text-primary);
        }

        /* Terminal Typing Cursor */
        .v09-cursor {
            display: inline-block;
            width: 8px;
            height: 1em;
            background: var(--acc-cyan);
            vertical-align: middle;
            animation: blink 1s step-end infinite;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }
        
        /* Audio/Processing Wave Animation */
        .v09-processing-wave {
            display: flex;
            align-items: center;
            gap: 2px;
            height: 15px;
        }
        .v09-wave-bar {
            width: 3px;
            background: var(--acc-cyan);
            height: 100%;
            animation: waveAnim 1.2s ease-in-out infinite;
            border-radius: 2px;
        }
        .v09-wave-bar:nth-child(2) { animation-delay: 0.2s; }
        .v09-wave-bar:nth-child(3) { animation-delay: 0.4s; }
        .v09-wave-bar:nth-child(4) { animation-delay: 0.6s; }

        @keyframes waveAnim {
            0%, 100% { height: 4px; }
            50% { height: 15px; }
        }
        """

    def build_js(self) -> str:
        """Controller für View 09: Filtering und Staggered Animations."""
        return f"""
        /* ==========================================================================
           VIEW 09 CONTROLLER: AI TERMINAL LOGIC
           ========================================================================== */
        class View09Controller {{
            constructor() {{
                this.viewElement = document.getElementById('{self.view_id}');
                this.categories = {json.dumps(self.categories)};
                this.insights = {json.dumps(self.insights)};
                this.currentIndex = 0; // Filter index
                
                this.initEvents();
            }}

            initEvents() {{
                window.addEventListener('keydown', (e) => {{
                    if (!this.viewElement || !this.viewElement.classList.contains('is-active')) return;

                    if (e.key === 'ArrowRight') {{
                        e.stopPropagation();
                        this.switchCategory(1);
                    }} else if (e.key === 'ArrowLeft') {{
                        e.stopPropagation();
                        this.switchCategory(-1);
                    }}
                }}, true);
            }}

            switchCategory(direction) {{
                this.currentIndex += direction;
                if (this.currentIndex >= this.categories.length) this.currentIndex = 0;
                if (this.currentIndex < 0) this.currentIndex = this.categories.length - 1;
                
                this.renderState();
            }}

            renderState() {{
                const activeCat = this.categories[this.currentIndex];

                // Update UI Sidebar Filters
                document.querySelectorAll('.v09-filter-item').forEach((item, idx) => {{
                    item.classList.toggle('is-active', idx === this.currentIndex);
                }});

                // Filter Logic
                const cards = document.querySelectorAll('.v09-card');
                let visibleCount = 0;

                cards.forEach(card => {{
                    // Reset animations
                    card.classList.remove('is-animating');
                    card.classList.remove('is-visible');
                    
                    if (activeCat === 'ALL' || card.dataset.category === activeCat) {{
                        card.classList.add('is-visible');
                        
                        // Staggered Entrance Animation
                        setTimeout(() => {{
                            card.classList.add('is-animating');
                        }}, 50 + (visibleCount * 100)); // 100ms delay per card
                        
                        visibleCount++;
                    }}
                }});

                // Update processing text to reflect active filter
                const procText = document.getElementById('v09-processing-text');
                procText.innerText = activeCat === 'ALL' ? 'Monitoring Global Vectors...' : `Filtering: ${{activeCat}}`;
            }}
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            window.V09Controller = new View09Controller();
            setTimeout(() => window.V09Controller.renderState(), 2000);
        }});
        """

    def build_html(self) -> str:
        """Generiert das HTML für View 09 (Filter + Data Feed)."""
        
        # Generiere die Filter-Liste dynamisch
        filters_html = ""
        for idx, cat in enumerate(self.categories):
            count = len(self.insights) if cat == 'ALL' else sum(1 for i in self.insights if i['category'] == cat)
            active_class = "is-active" if idx == 0 else ""
            filters_html += f"""
                <li class="v09-filter-item {active_class}">
                    {cat} <span class="v09-filter-count">{count}</span>
                </li>
            """

        # Generiere die Insight-Cards dynamisch
        cards_html = ""
        for idx, item in enumerate(self.insights):
            cards_html += f"""
                <div class="v09-card" data-category="{item['category']}" data-severity="{item['severity']}">
                    <div class="v09-card-header">
                        <span class="v09-timestamp">[{item['timestamp']}]</span>
                        <span class="v09-category-tag">{item['category']}</span>
                    </div>
                    <h3 class="v09-card-title">{item['title']}</h3>
                    <div class="v09-card-body">
                        {item['text']}
                        {"<span class='v09-cursor'></span>" if idx == 0 else ""}
                    </div>
                    <div class="v09-card-footer">
                        <button class="v09-btn-action">> {item['action']}</button>
                        <span class="v09-metric-highlight">{item['metric']}</span>
                    </div>
                </div>
            """

        return f"""
        <section class="view-container" id="view-09">
            
            <style>
                {self.build_css()}
            </style>

            <div class="v09-sidebar">
                <div>
                    <h2 style="font-size: 2rem; font-weight: 300; margin-bottom: 0.5rem; line-height: 1.1;">
                        Generative <span class="font-mono text-accent">Data Storytelling</span>
                    </h2>
                    <p class="text-secondary" style="font-size: 0.9rem;">
                        LLM-gestützter Narrative Layer. Das System synthetisiert Anomalien, KPIs und Marktdaten zu handlungsrelevanten Text-Insights.
                        <br><br>Stream filtern mit <kbd class="font-mono text-primary" style="background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">&larr;</kbd> <kbd class="font-mono text-primary" style="background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">&rarr;</kbd>.
                    </p>
                </div>

                <div class="kpi-card" style="margin-top: var(--space-sm); padding: var(--space-md); border-top: 1px solid rgba(0, 240, 255, 0.3);">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--space-sm);">
                        <div class="font-mono" style="font-size: 0.75rem; color: var(--acc-cyan);">ENGINE STATUS</div>
                        <div class="v09-processing-wave">
                            <div class="v09-wave-bar"></div><div class="v09-wave-bar"></div><div class="v09-wave-bar"></div><div class="v09-wave-bar"></div>
                        </div>
                    </div>
                    <div id="v09-processing-text" class="font-mono text-secondary" style="font-size: 0.8rem;">
                        Monitoring Global Vectors...
                    </div>
                </div>

                <ul class="v09-filter-list">
                    {filters_html}
                </ul>
            </div>

            <div class="v09-feed-container" id="v09-feed">
                <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 100px; background: linear-gradient(transparent, var(--bg-base)); z-index: 10; pointer-events: none;"></div>
                
                {cards_html}
            </div>

            <script>
                {self.build_js()}
            </script>
        </section>
        """

    def get_output(self) -> str:
        return self.build_html()

if __name__ == "__main__":
    builder = AIInsightsBuilder()
    html_output = builder.get_output()
    print(html_output)