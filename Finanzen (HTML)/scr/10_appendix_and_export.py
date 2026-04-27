# ==============================================================================
# DATEINAME: 10_appendix_and_export.py
# VIEW: 10 - Data Lineage, Methodology & System Export
# ==============================================================================
"""
Dieses Skript generiert die zehnte und letzte reine Ansichtsseite (View 10).
Es ist der technische "Under the Hood" Abschluss der Präsentation: Das Appendix.
Hier werden die Datenquellen (Data Lineage), die ML-Modelle und eine 
interaktive Mock-Export-Funktion (Board Report Generation) präsentiert.
Das Design wechselt zu einer stark technisch-dokumentarischen Ästhetik.
"""

import json

class AppendixAndExportBuilder:
    def __init__(self):
        self.view_id = "view-10"
        
        # High-End Data Payload: Methodology Specs
        self.lineage_data = [
            {
                "id": "model_01",
                "name": "Predictive Cashflow (FCF)",
                "type": "ARIMA-GARCH Hybrid",
                "sources": ["ERP_Main (SAP S/4HANA)", "Treasury_API (Kyriba)", "ECB_Rates"],
                "accuracy": "94.2% (R²)",
                "last_train": "T-04:15:00",
                "details": "Modelliert lineare Abhängigkeiten via ARIMA und Volatilitäts-Cluster (Saisonalität) via GARCH(1,1). Trainingsdaten: Letzte 48 Monate, daily resolution."
            },
            {
                "id": "model_02",
                "name": "Credit Exposure / PD",
                "type": "XGBoost Classifier",
                "sources": ["CRM_Core (Salesforce)", "Dun&Bradstreet_API", "Mkt_Sentiment_NLP"],
                "accuracy": "96.8% (AUC-ROC)",
                "last_train": "T-12:00:00",
                "details": "Gradient Boosting Tree Architektur. Wichtet Zahlungshistorie (40%), Makro-Indikatoren (35%) und unstrukturierte Sentiment-Daten (25%)."
            },
            {
                "id": "model_03",
                "name": "EBITDA Risk (VaR)",
                "type": "Monte Carlo Engine",
                "sources": ["Commodity_Exchange_Feed", "FX_Realtime_Spot", "SupplyChain_Index"],
                "accuracy": "N=10,000 Iterations",
                "last_train": "Real-time",
                "details": "Stochastische Simulation basierend auf historischen Kovarianz-Matrizen der letzten 10 Jahre. 95% Confidence Interval für Tail-Risk Evaluierung."
            }
        ]

    def build_css(self) -> str:
        """CSS für Akkordeons, technische Tabellen und Export-Terminals."""
        return """
        /* ==========================================================================
           VIEW 10: APPENDIX & EXPORT STYLES
           ========================================================================== */
        #view-10 {
            display: grid;
            grid-template-columns: 1fr 350px;
            grid-gap: var(--space-xl);
            align-content: start;
            padding-top: var(--space-xl);
        }

        /* Accordion Structure */
        .v10-accordion-list {
            display: flex;
            flex-direction: column;
            gap: var(--space-sm);
        }

        .v10-accordion-item {
            background: var(--bg-surface);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 4px;
            overflow: hidden;
            transition: border-color var(--duration-fast);
        }

        .v10-accordion-item.is-active {
            border-color: var(--acc-cyan);
            box-shadow: 0 0 15px rgba(0,240,255,0.05);
        }

        .v10-accordion-header {
            padding: var(--space-md);
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            background: rgba(255,255,255,0.02);
        }

        .v10-accordion-header:hover {
            background: rgba(255,255,255,0.05);
        }

        .v10-accordion-title {
            font-size: 1.1rem;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: var(--space-sm);
        }

        .v10-accordion-title::before {
            content: '>';
            color: var(--acc-cyan);
            font-family: var(--font-mono);
            transition: transform var(--duration-fast);
        }

        .v10-accordion-item.is-active .v10-accordion-title::before {
            transform: rotate(90deg);
        }

        .v10-accordion-body {
            max-height: 0;
            overflow: hidden;
            transition: max-height var(--duration-medium) var(--ease-out-expo);
            background: var(--bg-base);
        }

        .v10-accordion-content {
            padding: var(--space-md);
            border-top: 1px solid rgba(255,255,255,0.05);
        }

        /* Tech Data Tables */
        .v10-tech-table {
            width: 100%;
            border-collapse: collapse;
            font-family: var(--font-mono);
            font-size: 0.8rem;
        }

        .v10-tech-table th, .v10-tech-table td {
            text-align: left;
            padding: 8px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }

        .v10-tech-table th {
            color: var(--text-tertiary);
            font-weight: 400;
            text-transform: uppercase;
        }

        .v10-tech-table td {
            color: var(--text-secondary);
        }

        /* Source Tags */
        .v10-source-tag {
            display: inline-block;
            background: rgba(255,255,255,0.05);
            padding: 2px 6px;
            border-radius: 4px;
            margin-right: 4px;
            margin-bottom: 4px;
            font-size: 0.7rem;
            color: var(--acc-cyan);
            border: 1px solid rgba(0,240,255,0.2);
        }

        /* Export Panel */
        .v10-export-panel {
            background: var(--bg-surface-elevated);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            padding: var(--space-lg);
            display: flex;
            flex-direction: column;
            gap: var(--space-md);
        }

        .v10-btn {
            background: var(--bg-surface);
            border: 1px solid var(--text-tertiary);
            color: var(--text-primary);
            padding: var(--space-md);
            border-radius: 4px;
            font-family: var(--font-mono);
            font-size: 0.9rem;
            cursor: pointer;
            transition: all var(--duration-fast);
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            position: relative;
            overflow: hidden;
        }

        .v10-btn:hover {
            border-color: var(--acc-cyan);
            box-shadow: 0 0 15px rgba(0,240,255,0.15);
        }

        .v10-btn.btn-primary {
            background: rgba(0,240,255,0.1);
            border-color: var(--acc-cyan);
            color: var(--acc-cyan);
        }

        .v10-btn.btn-primary:hover {
            background: rgba(0,240,255,0.2);
        }

        /* Export Progress Animation */
        .v10-progress-bar {
            position: absolute;
            bottom: 0; left: 0; height: 3px;
            background: var(--acc-cyan);
            width: 0%;
            transition: width 2s linear;
        }

        .v10-terminal-log {
            font-family: var(--font-mono);
            font-size: 0.7rem;
            color: var(--text-tertiary);
            background: #000;
            padding: var(--space-sm);
            border-radius: 4px;
            height: 80px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
        }
        
        .v10-log-line {
            margin-top: 2px;
            animation: slideUpFade 0.3s forwards;
        }
        
        @keyframes slideUpFade {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        """

    def build_js(self) -> str:
        """Controller für Akkordeon-Logik und den interaktiven Export-Prozess."""
        return f"""
        /* ==========================================================================
           VIEW 10 CONTROLLER: APPENDIX & EXPORT LOGIC
           ========================================================================== */
        class View10Controller {{
            constructor() {{
                this.viewElement = document.getElementById('{self.view_id}');
                this.isExporting = false;
                
                this.initEvents();
            }}

            initEvents() {{
                // Accordion Setup
                const accordions = document.querySelectorAll('.v10-accordion-header');
                accordions.forEach(acc => {{
                    acc.addEventListener('click', (e) => this.toggleAccordion(e.currentTarget.parentElement));
                }});
                
                // Open first accordion by default
                if(document.querySelector('.v10-accordion-item')) {{
                    this.toggleAccordion(document.querySelector('.v10-accordion-item'));
                }}

                // Export Button Setup
                const exportBtn = document.getElementById('v10-btn-export');
                if(exportBtn) {{
                    exportBtn.addEventListener('click', () => this.triggerExport());
                }}
            }}

            toggleAccordion(item) {{
                const body = item.querySelector('.v10-accordion-body');
                const isActive = item.classList.contains('is-active');

                // Close all others
                document.querySelectorAll('.v10-accordion-item').forEach(other => {{
                    other.classList.remove('is-active');
                    other.querySelector('.v10-accordion-body').style.maxHeight = null;
                }});

                if (!isActive) {{
                    item.classList.add('is-active');
                    body.style.maxHeight = body.scrollHeight + "px";
                }}
            }}

            triggerExport() {{
                if (this.isExporting) return;
                this.isExporting = true;

                const btn = document.getElementById('v10-btn-export');
                const bar = btn.querySelector('.v10-progress-bar');
                const text = document.getElementById('v10-btn-text');
                const log = document.getElementById('v10-terminal');

                // Reset
                log.innerHTML = '';
                bar.style.transition = 'none';
                bar.style.width = '0%';
                
                setTimeout(() => {{
                    bar.style.transition = 'width 2.5s ease-out';
                    bar.style.width = '100%';
                    text.innerText = "COMPILING REPORT...";
                    btn.style.pointerEvents = 'none';
                }}, 50);

                const logs = [
                    "Initializing PDF Engine...",
                    "Flattening SVG architectures...",
                    "Injecting High-Res Canvas models...",
                    "Compiling Board-Ready Executive Summary...",
                    "Encrypting payload (AES-256)...",
                    "SUCCESS: Document Generated."
                ];

                logs.forEach((msg, i) => {{
                    setTimeout(() => {{
                        const line = document.createElement('div');
                        line.className = 'v10-log-line';
                        line.innerText = `> ${{msg}}`;
                        if (i === logs.length - 1) line.style.color = 'var(--acc-green)';
                        log.appendChild(line);
                    }}, i * 400);
                }});

                // Finish
                setTimeout(() => {{
                    text.innerText = "DOWNLOAD BOARD REPORT";
                    text.style.color = 'var(--acc-green)';
                    btn.style.borderColor = 'var(--acc-green)';
                    this.isExporting = false;
                    btn.style.pointerEvents = 'auto';
                    
                    setTimeout(() => {{
                        text.innerText = "GENERATE EXECUTIVE PDF";
                        text.style.color = '';
                        btn.style.borderColor = '';
                        bar.style.width = '0%';
                        bar.style.transition = 'none';
                    }}, 3000);
                }}, 2800);
            }}
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            window.V10Controller = new View10Controller();
        }});
        """

    def build_html(self) -> str:
        """Generiert das HTML für View 10 (Lineage + Export)."""
        
        # Dynamischer Aufbau der Modell-Akkordeons
        accordion_html = ""
        for idx, model in enumerate(self.lineage_data):
            sources_html = "".join([f'<span class="v10-source-tag">{s}</span>' for s in model["sources"]])
            
            accordion_html += f"""
            <div class="v10-accordion-item">
                <div class="v10-accordion-header">
                    <div class="v10-accordion-title">{model['name']}</div>
                    <div class="font-mono text-tertiary" style="font-size: 0.8rem;">{model['type']}</div>
                </div>
                <div class="v10-accordion-body">
                    <div class="v10-accordion-content">
                        <p class="text-secondary" style="font-size: 0.9rem; margin-bottom: var(--space-md);">{model['details']}</p>
                        <table class="v10-tech-table">
                            <tr>
                                <th>Data Ingestion Points</th>
                                <td>{sources_html}</td>
                            </tr>
                            <tr>
                                <th>Validation Metric</th>
                                <td class="font-mono text-primary">{model['accuracy']}</td>
                            </tr>
                            <tr>
                                <th>Last Checkpoint Sync</th>
                                <td class="font-mono text-primary">{model['last_train']}</td>
                            </tr>
                        </table>
                    </div>
                </div>
            </div>
            """

        return f"""
        <section class="view-container" id="view-10">
            
            <style>
                {self.build_css()}
            </style>

            <div>
                <h2 style="font-size: 2.5rem; font-weight: 300; margin-bottom: 0.5rem; line-height: 1.1;">
                    Data Lineage & <span class="font-mono text-accent">Methodology</span>
                </h2>
                <p class="text-secondary" style="font-size: 0.95rem; max-width: 600px; margin-bottom: var(--space-lg);">
                    Wissenschaftlicher Anhang zur Validierung der zugrundeliegenden Modelle. 
                    Transparenz über Datenquellen, Architekturen und Modellkonfidenz gem. Basel III / IFRS Vorgaben.
                </p>

                <div class="v10-accordion-list">
                    {accordion_html}
                </div>
                
                <div style="margin-top: var(--space-xl); padding-top: var(--space-md); border-top: 1px solid rgba(255,255,255,0.05); font-family: var(--font-mono); font-size: 0.7rem; color: var(--text-tertiary);">
                    © 2026 QUANTUM FINOPS ENGINE V1.0.0 // PREDICTIVE STATE: ACTIVE<br>
                    DEVELOPED FOR EXECUTIVE BOARD PRESENTATION PURPOSES.
                </div>
            </div>

            <div style="position: sticky; top: 100px;">
                <div class="v10-export-panel">
                    <div class="kpi-label">Artifact Generation</div>
                    
                    <p class="text-secondary" style="font-size: 0.85rem; line-height: 1.5; margin-bottom: var(--space-sm);">
                        Kompiliert den aktuellen Status, alle aktiven Szenarien und Forecasts in ein statisches, Board-fähiges PDF-Dokument.
                    </p>

                    <div class="v10-terminal-log" id="v10-terminal">
                        <div class="v10-log-line">> System Idle. Ready for compilation.</div>
                    </div>

                    <button class="v10-btn btn-primary" id="v10-btn-export" style="margin-top: var(--space-sm);">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                        <span id="v10-btn-text">GENERATE EXECUTIVE PDF</span>
                        <div class="v10-progress-bar"></div>
                    </button>

                    <button class="v10-btn">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="16" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
                        EXPORT RAW DATA (.CSV)
                    </button>
                </div>
                
                <div class="kpi-card" style="margin-top: var(--space-md); text-align: center;">
                    <div class="kpi-label">System Readiness</div>
                    <div class="font-mono" style="color: var(--acc-green); font-size: 1.5rem;">ALL SYSTEMS GO</div>
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
    builder = AppendixAndExportBuilder()
    html_output = builder.get_output()
    print(html_output)