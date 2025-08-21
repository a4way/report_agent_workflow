"""
Bericht-Generator-Agent für Fließtext-Berichte
"""
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from config import LLM_MODEL, TEMPERATURE, OPENAI_API_KEY


class ReportGeneratorAgent:
    """Agent für die Erstellung von Fließtext-Berichten aus KPI-Daten"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=0.3,  # Etwas höhere Temperatur für kreativen Text
            api_key=OPENAI_API_KEY
        )
        
        self.system_prompt = """
Du bist ein erfahrener Business Analyst und Berichtsschreiber. Deine Aufgabe ist es, aus KPI-Daten und Analysen professionelle, gut lesbare Berichte im Fließtext zu erstellen.

Deine Berichte sollen:
- Klar strukturiert sein (Einleitung, Hauptteil, Fazit)
- Konkrete Zahlen und KPIs einbeziehen
- Geschäftliche Insights und Handlungsempfehlungen enthalten
- In professionellem, aber verständlichem Deutsch verfasst sein
- Zwischen 200-500 Wörter lang sein
- Trends und Muster hervorheben
- Actionable Recommendations enthalten

Struktur:
1. Executive Summary (2-3 Sätze)
2. Wichtigste Erkenntnisse mit konkreten Zahlen
3. Trends und Auffälligkeiten
4. Handlungsempfehlungen
5. Ausblick

Verwende eine professionelle, aber zugängliche Sprache.
"""
    
    def generate_report(self, analysis_data: str, request_context: str = "") -> Dict[str, Any]:
        """
        Generiert einen Fließtext-Bericht aus KPI-Analysedaten
        """
        try:
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=f"""
Erstelle einen professionellen Geschäftsbericht basierend auf folgenden Analysedaten:

Kontext der ursprünglichen Anfrage: {request_context}

Analysedaten:
{analysis_data}

Erstelle einen strukturierten Bericht, der die wichtigsten Erkenntnisse hervorhebt und konkrete Handlungsempfehlungen gibt.
""")
            ]
            
            response = self.llm.invoke(messages)
            
            return {
                "status": "success",
                "report": response.content,
                "agent": "ReportGeneratorAgent",
                "word_count": len(response.content.split())
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "agent": "ReportGeneratorAgent"
            }
    
    def generate_executive_summary(self, full_report: str) -> Dict[str, Any]:
        """
        Erstellt eine Kurzzusammenfassung eines vollständigen Berichts
        """
        try:
            messages = [
                SystemMessage(content="""
Du erstellst prägnante Executive Summaries aus vollständigen Geschäftsberichten.
Die Zusammenfassung soll:
- Maximal 100 Wörter haben
- Die 3 wichtigsten Erkenntnisse enthalten
- Die wichtigste Handlungsempfehlung hervorheben
- Für C-Level Manager geeignet sein
"""),
                HumanMessage(content=f"""
Erstelle eine Executive Summary für folgenden Bericht:

{full_report}
""")
            ]
            
            response = self.llm.invoke(messages)
            
            return {
                "status": "success",
                "executive_summary": response.content,
                "agent": "ReportGeneratorAgent"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "agent": "ReportGeneratorAgent"
            } 