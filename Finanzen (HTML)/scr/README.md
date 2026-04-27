# Enterprise BI Dashboards: End-to-End Analytics

**Design-Philosophie:** Maximaler Informationsgehalt, absolutes Minimum an Rauschen. Jeder Pixel erfüllt einen Zweck.

Dieses Repository demonstriert den vollständigen Aufbau von Senior-Level Dashboards für vier Kernbereiche eines Unternehmens – von der Datengenerierung über die SQL-Transformation bis zur Visualisierung in vier verschiedenen Technologien.

### Preview
*(Hier im GitHub-Editor einfach dein HTML.mp4 Video und die 4 Bilder per Drag & Drop reinziehen)*
* [Video: Finanzen HTML Dashboard]
* [Screenshot: Produktion - Tableau]
* [Screenshot: Einkauf - PowerBI]
* [Screenshot: Marketing - Google Data Studio]

---

## 🛠 Tech Stack & Domains

| Abteilung | Technologie | Besonderheit |
| :--- | :--- | :--- |
| **Produktion** | Tableau | Custom Data Pipeline |
| **Einkauf** | PowerBI | SQL-basierte Transformation |
| **Marketing** | Google Data Studio | SaaS-Fokus |
| **Finanzen** | HTML / Python | Programmatisch generierte Single-Page-App |

---

## ⚙️ Data Workflow & Architektur

Ich habe nicht nur die Frontend-Dashboards gebaut, sondern die gesamte Backend-Pipeline simuliert:

### Standard-Pipeline (Tableau, PowerBI, GDS)
1. **Data Generation:** Eigene Python-Skripte (`generate_data_*.py`) erzeugen realistische Geschäftsdaten.
2. **Database:** Speicherung in relationalen SQLite-Datenbanken (`.db`).
3. **Transformation:** Erstellung der analytischen flachen Tabellen via SQL-Skripten.
4. **Visualization:** Import der sauberen Datenstrukturen in die BI-Tools.

### Custom-Pipeline (Finanzen HTML)
Das Finanz-Dashboard wurde komplett ohne klassisches BI-Tool von Grund auf programmiert:
* **Architektur:** 10 separate, modulare Python-Skripte im Backend.
* **Build-Prozess:** Ein `Builder.py`-Skript bündelt die Logik und rendert automatisiert eine hochperformante, >4.000 Zeilen starke HTML-Datei.

---

## 📂 Repository Struktur (Auszug)

Jeder Bereich ist strikt nach Data-Engineering-Best-Practices getrennt in `data` und `src` (Source Code):

```text
📦 BI-Dashboards
 ┣ 📂 Einkauf (PowerBI)
 ┃ ┣ 📂 Data (procurement.db, Transformation.sql)
 ┃ ┗ 📂 scr (generate_data_einkauf.py)
 ┣ 📂 Finanzen (HTML)
 ┃ ┣ 📂 scr (01_engine.py bis 10_appendix.py, Builder.py)
 ┃ ┗ 📜 FINAL_Dashboard_High_End.html
 ┣ 📂 Marketing (Google Data Studio)
 ┃ ┣ 📂 data (saas_data.db)
 ┃ ┗ 📂 scr (generate_data_marketing.py, transformation.sql)
 ┗ 📂 Produktion (Tableau)
   ┗ 📂 data (Maschine_data.db, generate_data_production.py)