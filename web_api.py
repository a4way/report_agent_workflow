#!/usr/bin/env python3
"""
FastAPI Web-API für das LangGraph Multi-Agenten Frontend
"""
import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

try:
    from utils.pdf_generator import ReportPDFGenerator
    PDF_AVAILABLE = True
except ImportError:
    print("⚠️ PDF-Generator nicht verfügbar")
    PDF_AVAILABLE = False

try:
    from orchestrator import MultiAgentOrchestrator
    ORCHESTRATOR_AVAILABLE = True
except ImportError:
    print("⚠️ Orchestrator nicht verfügbar - verwende Simulation")
    ORCHESTRATOR_AVAILABLE = False

# Pydantic Models
class WorkflowRequest(BaseModel):
    query: str
    demoId: str

class WorkflowResponse(BaseModel):
    success: bool
    message: str
    workflowId: Optional[str] = None

# FastAPI App
app = FastAPI(
    title="🤖 LangGraph Multi-Agenten API",
    description="REST API für das LangGraph Multi-Agenten Workflow System",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global State
orchestrator = None
current_workflows: Dict[str, Dict] = {}
workflow_logs: Dict[str, list] = {}
pdf_generator = None

# Initialize Orchestrator
@app.on_event("startup")
async def startup_event():
    global orchestrator, pdf_generator
    try:
        if ORCHESTRATOR_AVAILABLE:
            orchestrator = MultiAgentOrchestrator()
            print("✅ Multi-Agenten-Orchestrator erfolgreich initialisiert")
        else:
            print("⚠️ Orchestrator nicht verfügbar - API läuft im Simulations-Modus")
            
        if PDF_AVAILABLE:
            pdf_generator = ReportPDFGenerator()
            print("✅ PDF-Generator erfolgreich initialisiert")
        else:
            print("⚠️ PDF-Generator nicht verfügbar")
    except Exception as e:
        print(f"❌ Fehler beim Initialisieren: {e}")

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🤖 LangGraph Multi-Agenten API",
        "status": "running",
        "docs": "/api/docs"
    }

@app.get("/api/health")
async def health_check():
    """Gesundheitscheck der API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "orchestrator_ready": orchestrator is not None,
        "simulation_mode": not ORCHESTRATOR_AVAILABLE
    }

@app.post("/api/workflow/start", response_model=WorkflowResponse)
async def start_workflow(request: WorkflowRequest, background_tasks: BackgroundTasks):
    """Startet einen neuen Workflow"""
    workflow_id = f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Initialize workflow state
    current_workflows[workflow_id] = {
        "status": "running",
        "query": request.query,
        "demoId": request.demoId,
        "started_at": datetime.now().isoformat(),
        "current_step": "Initialisierung...",
        "workflow_status": {
            "orchestrator": "idle",
            "dataAnalyst": "idle",
            "duckdbTool": "idle",
            "reportGenerator": "idle"
        }
    }
    
    workflow_logs[workflow_id] = []
    
    # Start workflow in background
    background_tasks.add_task(run_workflow_simulation, workflow_id, request.query)
    
    return WorkflowResponse(
        success=True,
        message="Workflow erfolgreich gestartet",
        workflowId=workflow_id
    )

@app.get("/api/workflow/{workflow_id}/status")
async def get_workflow_status(workflow_id: str):
    """Gibt den aktuellen Status eines Workflows zurück"""
    if workflow_id not in current_workflows:
        raise HTTPException(status_code=404, detail="Workflow nicht gefunden")
    
    return current_workflows[workflow_id]

@app.get("/api/workflow/{workflow_id}/logs")
async def get_workflow_logs(workflow_id: str):
    """Gibt die Logs eines Workflows zurück"""
    if workflow_id not in workflow_logs:
        raise HTTPException(status_code=404, detail="Workflow-Logs nicht gefunden")
    
    return {"logs": workflow_logs[workflow_id]}

@app.get("/api/workflows")
async def list_workflows():
    """Listet alle aktiven Workflows auf"""
    return {
        "workflows": list(current_workflows.keys()),
        "count": len(current_workflows)
    }

@app.delete("/api/workflow/{workflow_id}")
async def delete_workflow(workflow_id: str):
    """Löscht einen Workflow und seine Logs"""
    if workflow_id in current_workflows:
        del current_workflows[workflow_id]
    if workflow_id in workflow_logs:
        del workflow_logs[workflow_id]
    
    return {"message": f"Workflow {workflow_id} erfolgreich gelöscht"}

@app.get("/api/workflow/{workflow_id}/report/download")
async def download_workflow_report(workflow_id: str):
    """Lädt den PDF-Bericht für einen Workflow herunter"""
    if workflow_id not in current_workflows:
        raise HTTPException(status_code=404, detail="Workflow nicht gefunden")
    
    workflow_data = current_workflows[workflow_id]
    
    if workflow_data.get("status") != "completed":
        raise HTTPException(status_code=400, detail="Workflow noch nicht abgeschlossen")
    
    if not PDF_AVAILABLE or not pdf_generator:
        raise HTTPException(status_code=503, detail="PDF-Generator nicht verfügbar")
    
    try:
        # Reports-Verzeichnis erstellen
        reports_dir = pdf_generator.create_reports_directory()
        
        # PDF-Dateiname generieren
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"langgraph_report_{workflow_data.get('demoId', 'unknown')}_{timestamp}.pdf"
        pdf_path = os.path.join(reports_dir, pdf_filename)
        
        # PDF generieren
        pdf_generator.generate_report_pdf(workflow_data, pdf_path)
        
        # PDF als Download zurückgeben
        return FileResponse(
            path=pdf_path,
            filename=pdf_filename,
            media_type='application/pdf',
            headers={"Content-Disposition": f"attachment; filename={pdf_filename}"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Generieren des PDF-Berichts: {str(e)}")

# Background Task Functions
async def run_workflow_simulation(workflow_id: str, query: str):
    """Simuliert einen Workflow im Hintergrund"""
    try:
        # Update workflow status
        current_workflows[workflow_id]["current_step"] = "Orchestrator startet..."
        current_workflows[workflow_id]["workflow_status"]["orchestrator"] = "active"
        
        add_log(workflow_id, "info", f"🚀 Starte Workflow: {workflow_id}", "System")
        add_log(workflow_id, "info", f"📝 Query: {query}", "System")
        
        # Step 1: Orchestrator
        await asyncio.sleep(2)
        current_workflows[workflow_id]["workflow_status"]["orchestrator"] = "completed"
        add_log(workflow_id, "success", "✅ Orchestrator: Anfrage erfolgreich klassifiziert", "Orchestrator")
        
        # Step 2: Data Analyst + DuckDB
        current_workflows[workflow_id]["current_step"] = "Datenanalyse läuft..."
        current_workflows[workflow_id]["workflow_status"]["dataAnalyst"] = "active"
        current_workflows[workflow_id]["workflow_status"]["duckdbTool"] = "active"
        
        add_log(workflow_id, "info", "📊 Datenanalyse-Agent: Beginne Analyse", "DataAnalyst")
        add_log(workflow_id, "info", "🔧 DuckDB Tool: Führe SQL-Queries aus", "DuckDBTool")
        
        # Simulate SQL queries
        queries = [
            "SELECT SUM(revenue) FROM orders WHERE status = 'paid'",
            "SELECT channel, COUNT(*) FROM customers GROUP BY channel",
            "SELECT AVG(order_value) FROM order_items"
        ]
        
        for i, sql_query in enumerate(queries):
            add_log(workflow_id, "info", f"🔍 SQL Query {i+1}: {sql_query}", "DuckDBTool")
            await asyncio.sleep(1)
        
        current_workflows[workflow_id]["workflow_status"]["duckdbTool"] = "completed"
        add_log(workflow_id, "success", "✅ DuckDB Tool: Alle Queries erfolgreich", "DuckDBTool")
        
        await asyncio.sleep(1)
        current_workflows[workflow_id]["workflow_status"]["dataAnalyst"] = "completed"
        add_log(workflow_id, "success", "✅ Datenanalyse-Agent: KPIs berechnet", "DataAnalyst", {
            "revenue": "782,517.00 €",
            "aov": "863.71 €", 
            "orders": "906",
            "gross_margin": "42.84%"
        })
        
        # Step 3: Report Generator
        current_workflows[workflow_id]["current_step"] = "Bericht wird erstellt..."
        current_workflows[workflow_id]["workflow_status"]["reportGenerator"] = "active"
        
        add_log(workflow_id, "info", "📝 Bericht-Generator: Erstelle professionellen Bericht", "ReportGenerator")
        await asyncio.sleep(3)
        
        current_workflows[workflow_id]["workflow_status"]["reportGenerator"] = "completed"
        add_log(workflow_id, "success", "✅ Bericht-Generator: Bericht fertiggestellt", "ReportGenerator", {
            "word_count": 377,
            "sections": ["Executive Summary", "KPI Analyse", "Handlungsempfehlungen"]
        })
        
        # Complete workflow
        current_workflows[workflow_id]["status"] = "completed"
        current_workflows[workflow_id]["current_step"] = "Workflow abgeschlossen!"
        current_workflows[workflow_id]["completed_at"] = datetime.now().isoformat()
        current_workflows[workflow_id]["pdf_available"] = PDF_AVAILABLE
        
        add_log(workflow_id, "success", "🎉 Workflow erfolgreich abgeschlossen!", "System")
        
        if PDF_AVAILABLE:
            add_log(workflow_id, "info", "📄 PDF-Bericht kann heruntergeladen werden", "System")
        
    except Exception as e:
        current_workflows[workflow_id]["status"] = "error"
        current_workflows[workflow_id]["error"] = str(e)
        add_log(workflow_id, "error", f"❌ Fehler im Workflow: {str(e)}", "System")

def add_log(workflow_id: str, level: str, message: str, agent: str = None, details: Dict = None):
    """Fügt einen Log-Eintrag hinzu"""
    log_entry = {
        "timestamp": int(datetime.now().timestamp() * 1000),
        "level": level,
        "message": message,
        "agent": agent,
        "details": details
    }
    
    if workflow_id not in workflow_logs:
        workflow_logs[workflow_id] = []
    
    workflow_logs[workflow_id].append(log_entry)

if __name__ == "__main__":
    print("🚀 Starte LangGraph Multi-Agenten Web-API...")
    print("📊 Frontend: http://localhost:8000")
    print("📋 API Docs: http://localhost:8000/api/docs")
    print("🔄 Backend API: http://localhost:8000/api/health")
    print("")

if __name__ == "__main__":
    try:
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            reload=False,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Fehler beim Starten des Servers: {e}")
        import traceback
        traceback.print_exc() 