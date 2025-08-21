"""
DuckDB Tool für SQL-Queries auf CSV-Dateien
"""
import duckdb
import pandas as pd
from typing import Dict, Any, Optional
from langchain.tools import BaseTool
from pydantic import Field
import os
from config import CSV_FILES


class DuckDBQueryTool(BaseTool):
    """Tool für SQL-Queries auf CSV-Dateien mit DuckDB"""
    
    name: str = "duckdb_query"
    description: str = """
    Führt SQL-Queries auf E-Commerce CSV-Dateien aus.
    
    Verfügbare Tabellen:
    - customers: customer_id, signup_date, acquisition_channel, country, region, age_group
    - orders: order_id, customer_id, order_date, order_status, payment_method, device, country
    - order_items: order_item_id, order_id, product_id, quantity, unit_price, discount_amount, net_price, tax_amount
    - products: product_id, category, unit_cost, unit_price
    - marketing_spend: date, channel, campaign, spend
    - web_analytics_daily: date, channel, sessions, users, transactions, revenue
    
    Wichtige Joins:
    - orders.customer_id → customers.customer_id
    - order_items.order_id → orders.order_id
    - order_items.product_id → products.product_id
    
    Beispiel: SELECT COUNT(*) as total_orders FROM orders WHERE order_status = 'paid'
    """
    
    def _run(self, query: str) -> str:
        """Führt eine SQL-Query aus und gibt das Ergebnis zurück"""
        try:
            # DuckDB-Verbindung erstellen
            conn = duckdb.connect(':memory:')
            
            # CSV-Dateien als Tabellen laden
            for table_name, file_path in CSV_FILES.items():
                if os.path.exists(file_path):
                    conn.execute(f"""
                        CREATE TABLE {table_name} AS 
                        SELECT * FROM read_csv_auto('{file_path}')
                    """)
            
            # Query ausführen
            result = conn.execute(query).fetchdf()
            
            # Verbindung schließen
            conn.close()
            
            # Ergebnis als String formatieren
            if result.empty:
                return "Keine Daten gefunden."
            
            # Für kleine Ergebnisse: vollständige Ausgabe
            if len(result) <= 20 and len(result.columns) <= 10:
                return result.to_string(index=False)
            
            # Für große Ergebnisse: Zusammenfassung
            summary = f"Query erfolgreich ausgeführt. {len(result)} Zeilen, {len(result.columns)} Spalten.\n"
            summary += f"Spalten: {', '.join(result.columns)}\n\n"
            summary += "Erste 10 Zeilen:\n"
            summary += result.head(10).to_string(index=False)
            
            if len(result) > 10:
                summary += f"\n\n... und {len(result) - 10} weitere Zeilen"
                
            return summary
            
        except Exception as e:
            return f"Fehler beim Ausführen der Query: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async-Version des Tools"""
        return self._run(query) 