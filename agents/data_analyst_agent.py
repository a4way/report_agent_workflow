"""
Datenanalyse-Agent für KPI-Berechnung
"""
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from tools.duckdb_tool import DuckDBQueryTool
from config import LLM_MODEL, TEMPERATURE, OPENAI_API_KEY


class DataAnalystAgent:
    """Agent für Datenanalyse und KPI-Berechnung"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=TEMPERATURE,
            api_key=OPENAI_API_KEY
        )
        self.duckdb_tool = DuckDBQueryTool()
        
        self.system_prompt = """
Du bist ein erfahrener Datenanalyst. Deine Aufgabe ist es, E-Commerce-Daten zu analysieren und wichtige KPIs zu berechnen.

Verfügbare KPIs und Berechnungen:
- Revenue: SUM(order_items.(net_price + tax_amount) * quantity) für bezahlte Bestellungen
- AOV (Average Order Value): Revenue / Anzahl Transaktionen für bezahlte Bestellungen  
- Conversion Rate: Transaktionen / Sessions (aus Web Analytics)
- ROAS (Return on Ad Spend): Revenue / Marketing Spend nach Kanal
- CAC (Customer Acquisition Cost): Marketing Spend / Neue Kunden nach Kanal
- Gross Margin: (Revenue - COGS) / Revenue, wobei COGS = SUM(products.unit_cost * quantity)

Gehe systematisch vor:
1. Verstehe die Anfrage
2. Führe die notwendigen SQL-Queries aus
3. Berechne die relevanten KPIs
4. Fasse die Ergebnisse strukturiert zusammen

Antworte immer auf Deutsch und gib konkrete Zahlen mit Erklärungen zurück.
"""
    
    def analyze_data(self, request: str) -> Dict[str, Any]:
        """
        Analysiert Daten basierend auf einer Anfrage und berechnet relevante KPIs
        """
        try:
            # Anfrage an LLM mit System-Prompt
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=f"""
Analysiere die folgenden Daten und berechne relevante KPIs:

Anfrage: {request}

Führe die notwendigen SQL-Queries aus und berechne die entsprechenden KPIs.
Strukturiere deine Antwort wie folgt:
1. Verständnis der Anfrage
2. Durchgeführte Analysen (mit SQL-Queries)
3. Berechnete KPIs mit konkreten Zahlen
4. Kurze Interpretation der Ergebnisse
""")
            ]
            
            # LLM-Response mit Tool-Verwendung
            response = self._analyze_with_tools(messages)
            
            return {
                "status": "success",
                "analysis": response,
                "agent": "DataAnalystAgent"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "agent": "DataAnalystAgent"
            }
    
    def _analyze_with_tools(self, messages: List) -> str:
        """
        Führt die Analyse mit verfügbaren Tools durch
        """
        # Erste LLM-Antwort um zu verstehen, welche Queries benötigt werden
        initial_response = self.llm.invoke(messages)
        
        # Extrahiere SQL-Queries aus der Antwort (vereinfachte Implementierung)
        analysis_text = initial_response.content
        
        # Beispiel-Queries für häufige KPIs
        common_queries = {
            "revenue": """
                SELECT SUM((oi.net_price + oi.tax_amount) * oi.quantity) as total_revenue
                FROM order_items oi
                JOIN orders o ON oi.order_id = o.order_id
                WHERE o.order_status = 'paid'
            """,
            "aov": """
                SELECT 
                    SUM((oi.net_price + oi.tax_amount) * oi.quantity) / COUNT(DISTINCT o.order_id) as aov
                FROM order_items oi
                JOIN orders o ON oi.order_id = o.order_id
                WHERE o.order_status = 'paid'
            """,
            "orders_by_channel": """
                SELECT 
                    c.acquisition_channel,
                    COUNT(DISTINCT o.order_id) as orders,
                    SUM((oi.net_price + oi.tax_amount) * oi.quantity) as revenue
                FROM orders o
                JOIN customers c ON o.customer_id = c.customer_id
                JOIN order_items oi ON o.order_id = oi.order_id
                WHERE o.order_status = 'paid'
                GROUP BY c.acquisition_channel
                ORDER BY revenue DESC
            """,
            "gross_margin": """
                SELECT 
                    SUM((oi.net_price + oi.tax_amount) * oi.quantity) as revenue,
                    SUM(p.unit_cost * oi.quantity) as cogs,
                    (SUM((oi.net_price + oi.tax_amount) * oi.quantity) - SUM(p.unit_cost * oi.quantity)) / 
                    SUM((oi.net_price + oi.tax_amount) * oi.quantity) * 100 as gross_margin_percent
                FROM order_items oi
                JOIN orders o ON oi.order_id = o.order_id
                JOIN products p ON oi.product_id = p.product_id
                WHERE o.order_status = 'paid'
            """
        }
        
        # Führe relevante Queries aus
        query_results = {}
        for query_name, query in common_queries.items():
            try:
                result = self.duckdb_tool._run(query)
                query_results[query_name] = result
            except Exception as e:
                query_results[query_name] = f"Fehler: {str(e)}"
        
        # Erstelle finale Analyse mit Query-Ergebnissen
        final_messages = messages + [
            initial_response,
            HumanMessage(content=f"""
Hier sind die Ergebnisse der SQL-Queries:

{chr(10).join([f"{name}: {result}" for name, result in query_results.items()])}

Erstelle jetzt eine strukturierte Analyse mit konkreten KPIs und deren Interpretation.
""")
        ]
        
        final_response = self.llm.invoke(final_messages)
        return final_response.content 