# Enterprise BI Dashboards: End-to-End Analytics

**Philosophie:** Maximaler Informationsgehalt, absolutes Minimum an Rauschen. Jeder Pixel hat einen Zweck.

## Preview
<div align="center">
  <video controls width="100%">
    <source src="Dashboard%20Vorschau/HTML.mp4" type="video/mp4">
    Ihr Browser unterstützt kein Video-Tag.
  </video>
  <br><br>
  
  <img src="Dashboard%20Vorschau/Google%20Data%20Studio.png" alt="Google Data Studio - Marketing" width="100%"/><br>
  <img src="Dashboard%20Vorschau/PowerBI.png" alt="PowerBI - Einkauf" width="100%"/><br>
  <img src="Dashboard%20Vorschau/Tableau.png" alt="Tableau - Produktion" width="100%"/>
</div>

***

## Project Workflow

Diese Senior-Level End-to-End BI-Lösung für vier Kernbereiche (Finanzen, Marketing, Einkauf, Produktion) deckt den gesamten Datenlebenszyklus ab:

1. **Synthetische Datengenerierung:** Eigene Python-Skripte (`generate_data_*.py`).
2. **Datenbank:** Relationale SQLite (`.db`).
3. **Transformation:** Analytische Datenansichten via SQL.
4. **Visualisierung:** Import in BI-Tools oder programmatisches Rendering.

### Core Stack
* **BI-Tools:** PowerBI, Tableau, Google Data Studio
* **Engineering:** Python, SQL (SQLite)
* **Benutzerdefinierte Lösung:** Eine modulare Python-Architektur bündelt Logik und automatisiert eine hochperformante, >4.000 Zeilen starke HTML-Datei für Finanzen.