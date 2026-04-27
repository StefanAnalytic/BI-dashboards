import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, timedelta
import random
import os
import uuid

# 1. Ziel-Ordner und DB-Pfad
db_dir = "/Users/stefanbechthold/Desktop/desktop/Bi tools/Produktion/data"
os.makedirs(db_dir, exist_ok=True) 
db_path = os.path.join(db_dir, "Maschine_data.db")

np.random.seed(42)
start_date = datetime.now() - timedelta(days=180)
end_date = datetime.now()

# ==========================================
# TABELLE 1: dim_maschinen (Stammdaten)
# ==========================================
maschinen_data = {
    'Maschinen_ID': [f"ROB-0{i}" for i in range(1, 6)],
    'Modell': ['KUKA KR IONTEC', 'KUKA KR QUANTEC', 'ABB IRB 6700', 'ABB IRB 6700', 'FANUC R-2000'],
    'Halle': ['Halle A', 'Halle A', 'Halle B', 'Halle B', 'Halle C'],
    'Inbetriebnahme_Jahr': [2018, 2019, 2021, 2021, 2017],
    'Wartungszyklus_Tage': [90, 90, 120, 120, 60]
}
df_maschinen = pd.DataFrame(maschinen_data)

# ==========================================
# TABELLE 2: dim_schichten (Für Radial Chart)
# ==========================================
schichten_data = {
    'Schicht_ID': ['S1', 'S2', 'S3'],
    'Schicht_Name': ['Frühschicht', 'Spätschicht', 'Nachtschicht'],
    'Start_Stunde': [6, 14, 22],
    'End_Stunde': [14, 22, 6],
    'Schichtleiter': ['Müller', 'Schmidt', 'Weber']
}
df_schichten = pd.DataFrame(schichten_data)

# ==========================================
# TABELLE 3 & 4: fact_sensor_log & fact_stoerungen
# ==========================================
bauteile = ["Gelenkarm", "Schweißkopf", "Kühlmodul", "Servomotor", "Steuerungseinheit"]
auswirkungen = ["Bandstillstand", "Gedrosselte Leistung", "Ausschuss produziert"]
fehlercodes = ["ERR-404", "WARN-102", "ERR-999", "WARN-305", "FATAL-001"]

date_rng = pd.date_range(start=start_date, end=end_date, freq='h') # h statt H
sensor_data = []
stoerung_data = []

for dt in date_rng:
    for maschine in df_maschinen['Maschinen_ID']:
        # Normale Sensorwerte
        vibration = np.random.normal(loc=2.5, scale=0.5) 
        temperatur = np.random.normal(loc=65.0, scale=5.0)
        strom_kw = np.random.normal(loc=15.0, scale=1.2)
        druck_bar = np.random.normal(loc=6.0, scale=0.2)
        
        # Anomalie / Störung? (ca. 2% Wahrscheinlichkeit)
        if random.random() < 0.02:
            # Sensoren schlagen aus
            vibration = np.random.normal(loc=8.5, scale=2.0)
            temperatur = np.random.normal(loc=105.0, scale=15.0)
            strom_kw = np.random.normal(loc=22.0, scale=3.0)
            druck_bar = np.random.normal(loc=3.0, scale=1.5)
            
            # Störungs-Event generieren
            stoerung_id = str(uuid.uuid4())[:8]
            bauteil = random.choice(bauteile)
            auswirkung = random.choice(auswirkungen)
            
            # Nachtschicht = öfter Totalausfall
            if dt.hour >= 22 or dt.hour <= 5:
                auswirkung = "Bandstillstand"
                
            stillstand_min = random.randint(15, 180) if auswirkung == "Bandstillstand" else 0
            kosten = round(stillstand_min * 45.50 + random.randint(100, 5000), 2) if stillstand_min > 0 else 0
            
            stoerung_data.append([
                stoerung_id, dt, maschine, random.choice(fehlercodes), 
                bauteil, auswirkung, stillstand_min, kosten
            ])

        sensor_data.append([dt, maschine, round(vibration, 2), round(temperatur, 1), round(strom_kw, 2), round(druck_bar, 2)])

df_sensor = pd.DataFrame(sensor_data, columns=['Timestamp', 'Maschinen_ID', 'Vibration_mm_s', 'Temperatur_C', 'Stromverbrauch_kW', 'Oeldruck_bar'])
df_stoerung = pd.DataFrame(stoerung_data, columns=['Stoerung_ID', 'Timestamp', 'Maschinen_ID', 'Fehlercode', 'Betroffenes_Bauteil', 'Auswirkung', 'Stillstand_Minuten', 'Reparaturkosten_EUR'])

# Unsauberkeiten einbauen (Nur bei Sensoren)
messy_indices = df_sensor.sample(frac=0.04).index
df_sensor.loc[messy_indices, 'Temperatur_C'] = np.nan
df_sensor.loc[df_sensor.sample(frac=0.02).index, 'Oeldruck_bar'] = np.nan

# ==========================================
# 5. In SQLite speichern
# ==========================================
conn = sqlite3.connect(db_path)
df_maschinen.to_sql('dim_maschinen', conn, if_exists='replace', index=False)
df_schichten.to_sql('dim_schichten', conn, if_exists='replace', index=False)
df_sensor.to_sql('fact_sensor_log', conn, if_exists='replace', index=False)
df_stoerung.to_sql('fact_stoerungen', conn, if_exists='replace', index=False)
conn.close()

print(f"Datenbank '{os.path.basename(db_path)}' mit 4 Tabellen erfolgreich erstellt!")