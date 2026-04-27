-- Wir zwingen die Zahlen in das deutsche Format (Komma statt Punkt)
CREATE TABLE dashboard_procurement_final_DE AS
SELECT 
    po.Order_ID,
    po.Order_Date,
    po.Material_ID,
    m.Category,
    COALESCE(po.Supplier_ID, 'UNKNOWN') AS Supplier_ID,
    ABS(po.Quantity) AS Quantity,
    
    -- Replace wandelt den Punkt in ein Komma um
    REPLACE(po.Actual_Price, '.', ',') AS Actual_Price,
    REPLACE(m.Standard_Price_EUR, '.', ',') AS Standard_Price_EUR,
    REPLACE(ROUND((po.Actual_Price - m.Standard_Price_EUR) * ABS(po.Quantity), 2), '.', ',') AS Total_PPV,
    REPLACE(ROUND((julianday(po.Order_Date) - julianday('2021-01-01')) / 365.0 * 0.12, 4), '.', ',') AS Market_Inflation_Trend
    
FROM raw_purchase_orders po
LEFT JOIN raw_material_master m ON po.Material_ID = m.Material_ID
WHERE po.Quantity > 0;