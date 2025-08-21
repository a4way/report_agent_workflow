"""
Konfiguration für den LangGraph Multi-Agenten Showcase
"""
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Konfiguration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY muss in der .env Datei gesetzt sein")

# Modell-Konfiguration
LLM_MODEL = "gpt-4o-mini"  # Kostengünstiger für Demo-Zwecke
TEMPERATURE = 0.1

# Pfade
DATA_PATH = "show_case_data"
CSV_FILES = {
    "customers": f"{DATA_PATH}/customers.csv",
    "orders": f"{DATA_PATH}/orders.csv", 
    "order_items": f"{DATA_PATH}/order_items.csv",
    "products": f"{DATA_PATH}/products.csv",
    "marketing_spend": f"{DATA_PATH}/marketing_spend.csv",
    "web_analytics_daily": f"{DATA_PATH}/web_analytics_daily.csv"
} 