"""
Orchestrator für den Multi-Agenten-Workflow
"""
from typing import Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from agents.data_analyst_agent import DataAnalystAgent
from agents.report_generator_agent import ReportGeneratorAgent
from tools.duckdb_tool import DuckDBQueryTool
from config import LLM_MODEL, TEMPERATURE, OPENAI_API_KEY


class WorkflowState(TypedDict):
    """State-Struktur für den LangGraph-Workflow"""
    original_request: str
    current_step: str
    analysis_result: Dict[str, Any]
    report_result: Dict[str, Any]
    final_output: str
    error: str


class MultiAgentOrchestrator:
    """Orchestrator für den Multi-Agenten-Workflow"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=TEMPERATURE,
            api_key=OPENAI_API_KEY
        )
        
        # Agenten initialisieren
        self.data_analyst = DataAnalystAgent()
        self.report_generator = ReportGeneratorAgent()
        self.duckdb_tool = DuckDBQueryTool()
        
        # Workflow-Graph erstellen
        self.workflow = self._create_workflow()
    
    def _create_workflow(self) -> StateGraph:
        """Erstellt den LangGraph-Workflow"""
        
        workflow = StateGraph(WorkflowState)
        
        # Knoten hinzufügen
        workflow.add_node("classify_request", self._classify_request)
        workflow.add_node("analyze_data", self._analyze_data)
        workflow.add_node("generate_report", self._generate_report)
        workflow.add_node("finalize_output", self._finalize_output)
        
        # Einstiegspunkt
        workflow.set_entry_point("classify_request")
        
        # Edges definieren
        workflow.add_edge("classify_request", "analyze_data")
        workflow.add_edge("analyze_data", "generate_report")
        workflow.add_edge("generate_report", "finalize_output")
        workflow.add_edge("finalize_output", END)
        
        return workflow.compile()
    
    def _classify_request(self, state: WorkflowState) -> WorkflowState:
        """Klassifiziert und verarbeitet die eingehende Anfrage"""
        try:
            request = state["original_request"]
            
            # Einfache Klassifizierung - kann erweitert werden
            classification_prompt = f"""
Analysiere folgende Geschäftsanfrage und kategorisiere sie:

Anfrage: {request}

Bestimme:
1. Welche Art von Analyse benötigt wird
2. Welche KPIs relevant sind
3. Welche Datentabellen verwendet werden sollten

Antworte kurz und präzise auf Deutsch.
"""
            
            messages = [
                SystemMessage(content="Du bist ein Business Intelligence Experte, der Datenanfragen klassifiziert."),
                HumanMessage(content=classification_prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            state["current_step"] = "request_classified"
            print(f"🎯 Anfrage klassifiziert: {response.content[:100]}...")
            
            return state
            
        except Exception as e:
            state["error"] = f"Fehler bei der Anfrage-Klassifizierung: {str(e)}"
            return state
    
    def _analyze_data(self, state: WorkflowState) -> WorkflowState:
        """Führt die Datenanalyse durch"""
        try:
            print("📊 Starte Datenanalyse...")
            
            analysis_result = self.data_analyst.analyze_data(state["original_request"])
            state["analysis_result"] = analysis_result
            state["current_step"] = "data_analyzed"
            
            if analysis_result["status"] == "success":
                print("✅ Datenanalyse erfolgreich abgeschlossen")
            else:
                print(f"❌ Fehler bei der Datenanalyse: {analysis_result.get('error', 'Unbekannter Fehler')}")
            
            return state
            
        except Exception as e:
            state["error"] = f"Fehler bei der Datenanalyse: {str(e)}"
            return state
    
    def _generate_report(self, state: WorkflowState) -> WorkflowState:
        """Generiert den Fließtext-Bericht"""
        try:
            print("📝 Generiere Bericht...")
            
            if state["analysis_result"]["status"] != "success":
                state["error"] = "Kann keinen Bericht erstellen - Datenanalyse war nicht erfolgreich"
                return state
            
            analysis_text = state["analysis_result"]["analysis"]
            report_result = self.report_generator.generate_report(
                analysis_text, 
                state["original_request"]
            )
            
            state["report_result"] = report_result
            state["current_step"] = "report_generated"
            
            if report_result["status"] == "success":
                print("✅ Bericht erfolgreich generiert")
            else:
                print(f"❌ Fehler bei der Berichtserstellung: {report_result.get('error', 'Unbekannter Fehler')}")
            
            return state
            
        except Exception as e:
            state["error"] = f"Fehler bei der Berichtserstellung: {str(e)}"
            return state
    
    def _finalize_output(self, state: WorkflowState) -> WorkflowState:
        """Finalisiert die Ausgabe"""
        try:
            print("🎁 Finalisiere Ausgabe...")
            
            if state.get("error"):
                state["final_output"] = f"❌ Fehler im Workflow: {state['error']}"
                return state
            
            if (state["analysis_result"]["status"] == "success" and 
                state["report_result"]["status"] == "success"):
                
                # Kombiniere Analyse und Bericht
                final_output = f"""
# 📊 Business Intelligence Bericht

## 🎯 Ihre Anfrage
{state['original_request']}

## 📈 Datenanalyse
{state['analysis_result']['analysis']}

## 📝 Executive Report
{state['report_result']['report']}

---
*Generiert durch Multi-Agenten-System mit LangGraph*
*Wörter im Bericht: {state['report_result'].get('word_count', 'N/A')}*
"""
                state["final_output"] = final_output
                print("✅ Workflow erfolgreich abgeschlossen")
            else:
                state["final_output"] = "❌ Workflow konnte nicht erfolgreich abgeschlossen werden"
            
            return state
            
        except Exception as e:
            state["error"] = f"Fehler bei der Finalisierung: {str(e)}"
            state["final_output"] = f"❌ Fehler bei der Finalisierung: {str(e)}"
            return state
    
    def process_request(self, request: str) -> str:
        """
        Hauptmethode zur Verarbeitung einer Geschäftsanfrage
        """
        print(f"🚀 Starte Multi-Agenten-Workflow für: {request[:50]}...")
        
        # Initial State
        initial_state = WorkflowState(
            original_request=request,
            current_step="starting",
            analysis_result={},
            report_result={},
            final_output="",
            error=""
        )
        
        try:
            # Workflow ausführen
            final_state = self.workflow.invoke(initial_state)
            return final_state["final_output"]
            
        except Exception as e:
            error_msg = f"❌ Kritischer Fehler im Orchestrator: {str(e)}"
            print(error_msg)
            return error_msg 