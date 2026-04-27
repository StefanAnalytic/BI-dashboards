import sqlite3
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Pfade anpassen
output_dir = "/Users/stefanbechthold/Desktop/Bi tools/Einkauf/Data"
db_path = os.path.join(output_dir, "procurement.db")
os.makedirs(output_dir, exist_ok=True)

conn = sqlite3.connect(db_path)

print(f"Erstelle intelligente Datenbank unter: {db_path}...")

# 1. Materialstamm
materials = [
    ('MAT-001', 'Steel', 120.00),
    ('MAT-002', 'Aluminum', 85.00),
    ('MAT-003', 'Copper', 450.00),
    ('MAT-004', 'Plastics', 25.00),
    ('MAT-005', 'Electronics', 890.00)
]
df_materials = pd.DataFrame(materials, columns=['Material_ID', 'Category', 'Standard_Price_EUR'])

# 2. Systematische Bestellungen generieren
num_orders = 5500
start_date = datetime(2021, 1, 1)
data_orders = []

suppliers = ['SUP-101', 'SUP-102', 'SUP-103', 'SUP-104']

for i in range(num_orders):
    order_date = start_date + timedelta(days=random.randint(0, 1095))
    mat = random.choice(materials)
    category = mat[1]
    base_price = mat[2]
    
    # STORY 1: Basis-Inflation (steigt leicht über 3 Jahre, ca. 15%)
    days_passed = (order_date - start_date).days
    market_inflation = 1 + (days_passed / 1095) * 0.15 
    
    # STORY 2: Die "Kupfer/Alu-Krise" (Mitte 2022 bis Ende 2022 gibt es einen extremen Preisschock)
    is_crisis = datetime(2022, 5, 1) <= order_date <= datetime(2022, 12, 31)
    if is_crisis and category in ['Copper', 'Aluminum']:
        market_inflation += 0.45 # 45% Preissprung in der Krise!
        
    actual_price = base_price * market_inflation
    
    # Lieferant auswählen
    supplier_id = random.choice(suppliers)
    
    # STORY 3: Lieferanten-Verhalten
    if supplier_id == 'SUP-102':
        # Strategischer Partner: Federt Marktschwankungen ab (nur halbe Inflation)
        actual_price = base_price + ((actual_price - base_price) * 0.5) 
    elif supplier_id == 'SUP-101' and is_crisis:
        # Opportunist: Schlägt in der Krise nochmal extra drauf
        actual_price = actual_price * 1.15 
        
    # STORY 4: Mengenrabatte & Maverick Buying
    qty = int(np.random.normal(200, 150)) # Normalverteilung um 200 Stück
    if qty < 10: qty = random.randint(10, 50) # Keine extremen Minuswerte generieren
    
    if qty > 400:
        actual_price = actual_price * 0.88 # 12% Rabatt für Großbestellungen
    elif qty < 50:
        actual_price = actual_price * 1.10 # 10% Aufschlag für Kleinstmengen (Maverick)

    # Etwas natürliches Rauschen hinzufügen (± 3%)
    actual_price = actual_price * random.uniform(0.97, 1.03)

    # --- Dirty Data für das SQL Cleaning ---
    if random.random() > 0.05:
        final_supplier = supplier_id
    else:
        final_supplier = None # 5% fehlende Lieferanten
        
    currency = random.choice(['EUR', 'eur', ' EUR ', '€', 'Euro'])
    
    # 2% Tippfehler bei der Menge (negativ)
    if random.random() < 0.02: 
        qty = qty * -1
        
    data_orders.append((
        f"PO-{10000 + i}", 
        order_date.strftime('%Y-%m-%d'), 
        mat[0], 
        final_supplier, 
        qty, 
        round(actual_price, 2), 
        currency
    ))

df_orders = pd.DataFrame(data_orders, columns=['Order_ID', 'Order_Date', 'Material_ID', 'Supplier_ID', 'Quantity', 'Actual_Price', 'Currency'])

# In SQL-Tabellen schreiben
df_materials.to_sql('raw_material_master', conn, if_exists='replace', index=False)
df_orders.to_sql('raw_purchase_orders', conn, if_exists='replace', index=False)

conn.close()
print("Erfolg! Die Datenbank mit stark korrelierten Business-Szenarien wurde erstellt.")