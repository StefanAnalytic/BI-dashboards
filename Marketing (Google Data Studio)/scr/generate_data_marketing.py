import sqlite3
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# 1. Ziel-Ordner und DB-Pfad
db_dir = "/Users/stefanbechthold/Desktop/Bi tools/Marketing/data"
os.makedirs(db_dir, exist_ok=True) 
db_path = os.path.join(db_dir, "saas_data.db")

campaigns = ["Winter_Sale_2023", "Influencer_Tech_Talk", "Google_Ads_Brand", "Facebk_Pro_v2", "Organic_Search"]
campaign_ids = ["CMP-001", "CMP-002", "CMP-003", "CMP-004", "CMP-005"]
start_date = datetime(2023, 1, 1)

marketing_data = []
user_data = []
user_counter = 10000

print("Generiere mathematisch perfekte Daten...")

# 2. Daten generieren (Marketing & Users synchron!)
for i, camp in enumerate(campaigns):
    # Facebk_Pro_v2 ist unser designierter Verlierer (hoher Churn)
    churn_prob = 0.7 if "Facebk" in camp else random.uniform(0.1, 0.3)
    
    for day in range(120): # 120 Tage
        current_date = start_date + timedelta(days=day)
        
        # Schmutz für GitHub: Datumsformate & Namen
        date_str = current_date.strftime("%Y-%m-%d") if random.random() > 0.2 else current_date.strftime("%d/%m/%Y")
        display_name = camp if random.random() > 0.1 else camp.replace("e", "3").replace("_", "-")
        
        spend = round(random.uniform(50, 500), 2)
        if random.random() < 0.05: spend = np.nan # Fehlende Budgets
        
        signups = random.randint(5, 50)
        clicks = signups * random.randint(20, 50)
        
        marketing_data.append([date_str, campaign_ids[i], display_name, spend, clicks, signups])
        
        # JETZT WICHTIG: Exakt so viele User generieren wie Signups!
        for _ in range(signups):
            user_id = f"U{user_counter}"
            user_counter += 1
            
            # Schmutz: Seltene Duplikate
            if random.random() < 0.01: user_id = f"U{user_counter-1}" 
            
            is_churned = random.random() < churn_prob
            churn_date = current_date + timedelta(days=random.randint(1, 30)) if is_churned else None
            
            activity_score = random.randint(1, 100)
            if random.random() < 0.01: activity_score = 999 # Ausreißer
            
            user_data.append([
                user_id, 
                current_date.strftime("%Y-%m-%d"), 
                churn_date.strftime("%Y-%m-%d") if churn_date else None, 
                activity_score, 
                campaign_ids[i]
            ])

df_marketing = pd.DataFrame(marketing_data, columns=["Date", "CampaignID", "CampaignName", "Spend", "Clicks", "Signups"])
df_users = pd.DataFrame(user_data, columns=["UserID", "SignupDate", "ChurnDate", "ActivityScore", "CampaignID"])

# 3. Direkt in SQLite speichern
conn = sqlite3.connect(db_path)
df_marketing.to_sql("marketing_raw", conn, if_exists="replace", index=False)
df_users.to_sql("users_raw", conn, if_exists="replace", index=False)
conn.close()

print(f"Erfolg! Datenbank 'saas_data.db' ist bereit für die SQL-Ansicht.")