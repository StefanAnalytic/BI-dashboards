# ==============================================================================
# DATEINAME: 01_engine_and_hero.py
# ==============================================================================
"""
Du hast absolut recht. Das vorherige Skript war konzeptionell, oberflächlich und eines 
Data Scientists auf Senior-Level nicht würdig. Keine Ausreden. Wenn wir ein +100k Agentur-
Produkt bauen, dann muss die Architektur von Zeile 1 an massiv, skalierbar und visuell 
beeindruckend sein. 

Dieses Skript ist der echte Startschuss (Iteration 1 von 10). 
Es baut die komplette Basis-Engine:
- Den Zero-Scroll State-Manager (Vanilla JS, Event-Debouncing für Wheel/Keyboard).
- Das globale High-End Design-System (CSS Variables, Deep Dark Mode, Typografie).
- Die View 01: Das Hero-Dashboard (Predictive FCF, Risk Exposure, Executive Summary).

Das Skript generiert sauberen, modularen Code, der in den nächsten Iterationen append-only 
erweitert wird. Welcome to the Agency Level.
"""

import datetime

class PresentationEngineBuilder:
    def __init__(self):
        self.project_name = "Predictive Corporate Finance Dashboard"
        self.version = "1.0.0"
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def build_css_design_system(self) -> str:
        """Erzeugt das fundamentale, wissenschaftliche Dark-Mode Design-System."""
        return """
        /* ==========================================================================
           DESIGN SYSTEM & CORE VARIABLES (AGENCY LEVEL)
           ========================================================================== */
        :root {
            /* Color Palette - Deep Scientific Dark */
            --bg-base: #060709;
            --bg-surface: #0D0F14;
            --bg-surface-elevated: #161922;
            --bg-glass: rgba(22, 25, 34, 0.6);
            
            /* Accents */
            --acc-cyan: #00F0FF;
            --acc-cyan-glow: rgba(0, 240, 255, 0.2);
            --acc-purple: #8A2BE2;
            --acc-amber: #FFB000;
            --acc-red: #FF3366;
            --acc-green: #00E676;
            
            /* Typography */
            --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-mono: 'Roboto Mono', 'Fira Code', monospace;
            
            /* Text Colors */
            --text-primary: #FFFFFF;
            --text-secondary: #8B94A5;
            --text-tertiary: #5A6270;
            
            /* Spacing & Layout */
            --space-xs: 0.25rem;
            --space-sm: 0.5rem;
            --space-md: 1rem;
            --space-lg: 2rem;
            --space-xl: 4rem;
            
            /* Z-Index Architecture */
            --z-background: 0;
            --z-view: 10;
            --z-overlay: 50;
            --z-nav: 100;
            --z-modal: 1000;
            
            /* Motion & Transitions */
            --ease-out-expo: cubic-bezier(0.19, 1, 0.22, 1);
            --ease-in-out-circ: cubic-bezier(0.785, 0.135, 0.15, 0.86);
            --duration-fast: 300ms;
            --duration-medium: 600ms;
            --duration-slow: 1200ms;
        }

        /* ==========================================================================
           GLOBAL RESETS & TYPOGRAPHY
           ========================================================================== */
        *, *::before, *::after {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body, html {
            width: 100vw;
            height: 100vh;
            overflow: hidden; /* ZERO SCROLL ARCHITECTURE */
            background-color: var(--bg-base);
            color: var(--text-primary);
            font-family: var(--font-sans);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            font-size: 16px;
            line-height: 1.5;
        }

        h1, h2, h3, h4, h5, h6 {
            font-weight: 300;
            letter-spacing: -0.02em;
        }

        .font-mono { font-family: var(--font-mono); }
        .text-accent { color: var(--acc-cyan); }
        .text-warning { color: var(--acc-amber); }
        .text-danger { color: var(--acc-red); }
        .text-success { color: var(--acc-green); }

        /* ==========================================================================
           LAYOUT ENGINE (VIEWS)
           ========================================================================== */
        #app-root {
            position: relative;
            width: 100%;
            height: 100%;
            display: flex;
        }

        /* Global HUD / Nav */
        .global-hud {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
            z-index: var(--z-nav);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: var(--space-lg);
        }

        .hud-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            padding-bottom: var(--space-md);
        }

        .hud-title {
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: var(--space-sm);
        }

        .hud-title::before {
            content: '';
            display: block;
            width: 8px; height: 8px;
            background: var(--acc-cyan);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--acc-cyan);
        }

        .view-container {
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            opacity: 0;
            visibility: hidden;
            transform: translateY(20px) scale(0.98);
            transition: opacity var(--duration-medium) var(--ease-out-expo),
                        transform var(--duration-medium) var(--ease-out-expo),
                        visibility var(--duration-medium);
            z-index: var(--z-view);
            padding: calc(var(--space-lg) * 3) var(--space-lg) var(--space-lg);
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            grid-gap: var(--space-md);
        }

        .view-container.is-active {
            opacity: 1;
            visibility: visible;
            transform: translateY(0) scale(1);
            pointer-events: auto;
        }

        /* ==========================================================================
           UI COMPONENTS: CARDS & WIDGETS
           ========================================================================== */
        .kpi-card {
            background: var(--bg-surface);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 4px;
            padding: var(--space-lg);
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
        }

        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 2px;
            background: linear-gradient(90deg, var(--acc-cyan), transparent);
            opacity: 0.5;
        }

        .kpi-label {
            font-size: 0.75rem;
            text-transform: uppercase;
            color: var(--text-secondary);
            margin-bottom: var(--space-sm);
            letter-spacing: 0.05em;
        }

        .kpi-value {
            font-size: 3rem;
            font-family: var(--font-mono);
            font-weight: 300;
            margin-bottom: var(--space-xs);
        }

        .kpi-trend {
            font-size: 0.875rem;
            display: flex;
            align-items: center;
            gap: var(--space-xs);
        }

        /* Grid Placements for View 01 */
        .v01-hero { grid-column: 1 / -1; margin-bottom: var(--space-lg); }
        .v01-kpi-1 { grid-column: 1 / 5; }
        .v01-kpi-2 { grid-column: 5 / 9; }
        .v01-kpi-3 { grid-column: 9 / 13; }
        .v01-main-chart { grid-column: 1 / 9; height: 400px; margin-top: var(--space-md); }
        .v01-side-panel { grid-column: 9 / 13; height: 400px; margin-top: var(--space-md); }
        """

    def build_js_state_manager(self) -> str:
        """Erzeugt die Vanilla JS Presentation Engine (Zero-Scroll, Pfeiltasten)."""
        return """
        /* ==========================================================================
           JS PRESENTATION ENGINE (Zero-Scroll State Manager)
           ========================================================================== */
        class QuantumPresentationEngine {
            constructor() {
                this.views = document.querySelectorAll('.view-container');
                this.totalViews = this.views.length;
                this.currentViewIndex = 0;
                this.isAnimating = false;
                
                // Config
                this.scrollCooldown = 1200; // ms
                
                this.init();
            }

            init() {
                this.updateDOM();
                this.bindEvents();
                console.log(`[Quantum Engine] Initialized. ${this.totalViews} views detected.`);
            }

            bindEvents() {
                // Keyboard Navigation
                window.addEventListener('keydown', (e) => {
                    if (this.isAnimating) return;
                    
                    if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
                        this.navigate(1);
                    } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
                        this.navigate(-1);
                    }
                });

                // Wheel Navigation (Debounced)
                window.addEventListener('wheel', (e) => {
                    if (this.isAnimating) return;

                    // Normalize wheel delta
                    const delta = Math.sign(e.deltaY);
                    if (delta > 0) {
                        this.navigate(1);
                    } else if (delta < 0) {
                        this.navigate(-1);
                    }
                }, { passive: false });
            }

            navigate(direction) {
                const nextIndex = this.currentViewIndex + direction;
                
                // Boundary check
                if (nextIndex < 0 || nextIndex >= this.totalViews) return;

                this.lockAnimation();
                this.currentViewIndex = nextIndex;
                this.updateDOM();
                this.updateHUD();
            }

            updateDOM() {
                this.views.forEach((view, index) => {
                    if (index === this.currentViewIndex) {
                        view.classList.add('is-active');
                        // Trigger inner view animations here later
                    } else {
                        view.classList.remove('is-active');
                    }
                });
            }

            updateHUD() {
                const indicator = document.getElementById('hud-progress-text');
                if(indicator) {
                    indicator.innerText = `[ VIEW ${String(this.currentViewIndex + 1).padStart(2, '0')} / ${String(this.totalViews).padStart(2, '0')} ]`;
                }
            }

            lockAnimation() {
                this.isAnimating = true;
                setTimeout(() => {
                    this.isAnimating = false;
                }, this.scrollCooldown);
            }
        }

        // Initialize when DOM is ready
        document.addEventListener('DOMContentLoaded', () => {
            window.AppEngine = new QuantumPresentationEngine();
        });
        """

    def build_view_01_hero(self) -> str:
        """Erzeugt das HTML-Markup für die erste Ansicht (Executive Hero)."""
        return """
        <section class="view-container is-active" id="view-01">
            
            <div class="v01-hero">
                <h1 style="font-size: 3.5rem; font-weight: 200; margin-bottom: 1rem;">
                    Global Financial <span class="text-accent font-mono" style="font-weight: 400;">State Engine</span>
                </h1>
                <p class="text-secondary" style="max-width: 600px; font-size: 1.1rem; line-height: 1.6;">
                    Predictive Cashflow, ML-based EBITDA Risk Exposure, and Real-Time Liquidity Allocation. 
                    Generated by AI Data Architectures.
                </p>
            </div>

            <div class="kpi-card v01-kpi-1">
                <div class="kpi-label">Predictive FCF (90 Days)</div>
                <div class="kpi-value">€142.5<span style="font-size:1.5rem; color:var(--text-tertiary)">M</span></div>
                <div class="kpi-trend text-success">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 6l-9.5 9.5-5-5L1 18"/><path d="M17 6h6v6"/></svg>
                    +12.4% vs Baseline (ARIMA Model)
                </div>
            </div>

            <div class="kpi-card v01-kpi-2" style="border-top-color: var(--acc-amber);">
                <div class="kpi-label text-warning">EBITDA at Risk (Monte Carlo, 95% CI)</div>
                <div class="kpi-value text-warning">€18.2<span style="font-size:1.5rem; color:var(--text-tertiary)">M</span></div>
                <div class="kpi-trend text-secondary">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                    Volatility driven by FX exposure (USD/EUR)
                </div>
            </div>

            <div class="kpi-card v01-kpi-3" style="border-top-color: var(--acc-purple);">
                <div class="kpi-label">Algorithmic Credit Exposure</div>
                <div class="kpi-value">2.4<span style="font-size:1.5rem; color:var(--text-tertiary)">%</span></div>
                <div class="kpi-trend text-secondary">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                    PD (Probability of Default) stable across Top 50 Clients.
                </div>
            </div>

            <div class="kpi-card v01-main-chart">
                <div class="kpi-label">Liquidity Trajectory & Anomaly Detection (Isolation Forest)</div>
                <div style="width: 100%; height: calc(100% - 30px); border-bottom: 1px solid var(--text-tertiary); position: relative; display: flex; align-items: flex-end;">
                    <svg width="100%" height="100%" preserveAspectRatio="none" viewBox="0 0 100 100">
                        <defs>
                            <linearGradient id="grad1" x1="0%" y1="0%" x2="0%" y2="100%">
                                <stop offset="0%" style="stop-color:var(--acc-cyan);stop-opacity:0.3" />
                                <stop offset="100%" style="stop-color:var(--bg-surface);stop-opacity:0" />
                            </linearGradient>
                        </defs>
                        <path d="M0,100 L0,50 Q25,30 50,60 T100,20 L100,100 Z" fill="url(#grad1)"/>
                        <path d="M0,50 Q25,30 50,60 T100,20" fill="none" stroke="var(--acc-cyan)" stroke-width="0.5"/>
                        <circle cx="75" cy="40" r="1.5" fill="var(--acc-amber)" class="pulse-anim" />
                    </svg>
                </div>
            </div>

            <div class="kpi-card v01-side-panel">
                <div class="kpi-label">System Diagnostics</div>
                <ul style="list-style: none; margin-top: 1rem; font-family: var(--font-mono); font-size: 0.8rem; color: var(--text-secondary);">
                    <li style="margin-bottom: 0.5rem; display: flex; justify-content: space-between;">
                        <span>Data Ingestion</span><span class="text-success">OK (12ms)</span>
                    </li>
                    <li style="margin-bottom: 0.5rem; display: flex; justify-content: space-between;">
                        <span>ARIMA Model Sync</span><span class="text-success">OK</span>
                    </li>
                    <li style="margin-bottom: 0.5rem; display: flex; justify-content: space-between;">
                        <span>Monte Carlo Iterations</span><span class="text-primary">10,000</span>
                    </li>
                    <li style="margin-bottom: 0.5rem; display: flex; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 0.5rem;">
                        <span>XGBoost Confidence</span><span class="text-accent">94.2%</span>
                    </li>
                </ul>
            </div>

        </section>
        """

    def build_full_html_document(self) -> str:
        """Fügt alles zusammen zu einem ausführbaren HTML-String."""
        css = self.build_css_design_system()
        js = self.build_js_state_manager()
        view_01 = self.build_view_01_hero()

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>High-End Finance Dashboard | DS Level</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;600&family=Roboto+Mono:wght@300;400&display=swap" rel="stylesheet">
    <style>
        {css}
    </style>
</head>
<body>

    <div class="global-hud">
        <div class="hud-header">
            <div class="hud-title font-mono">Quantum FinOps // Model Context</div>
            <div id="hud-progress-text" class="font-mono" style="color: var(--text-tertiary); font-size: 0.75rem;">[ VIEW 01 / 01 ]</div>
        </div>
        <div class="hud-footer">
            <div class="font-mono" style="font-size: 0.65rem; color: var(--text-tertiary);">
                USE ARROW KEYS OR SCROLL TO NAVIGATE SCENES
            </div>
        </div>
    </div>

    <div id="app-root">
        {view_01}
        </div>

    <script>
        {js}
    </script>
</body>
</html>
"""
        return html

if __name__ == "__main__":
    builder = PresentationEngineBuilder()
    generated_html = builder.build_full_html_document()
    
    # Im Entwicklungsmodus geben wir den Python-Code aus, der das HTML generiert.
    # Wenn dieser Code ausgeführt wird, druckt er das fertige HTML für View 1.
    print(generated_html)