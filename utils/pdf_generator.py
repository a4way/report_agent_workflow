"""
PDF-Generator für LangGraph Multi-Agenten Berichte
"""
import os
from datetime import datetime
from typing import Dict, Any
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import markdown
import re


class ReportPDFGenerator:
    """Generiert PDF-Berichte aus Workflow-Ergebnissen"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Erstellt benutzerdefinierte Styles"""
        # Title Style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#1e40af'),
            alignment=TA_CENTER
        ))
        
        # Subtitle Style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            textColor=HexColor('#3b82f6'),
            alignment=TA_LEFT
        ))
        
        # KPI Style
        self.styles.add(ParagraphStyle(
            name='KPIStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            textColor=HexColor('#059669'),
            fontName='Helvetica-Bold'
        ))
        
        # Body Style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            leading=14
        ))
    
    def generate_report_pdf(self, workflow_data: Dict[str, Any], output_path: str) -> str:
        """Generiert einen PDF-Bericht aus Workflow-Daten"""
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Story-Elemente sammeln
        story = []
        
        # Header
        story.append(Paragraph("🤖 LangGraph Multi-Agenten Analyse", self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Workflow Info
        story.append(Paragraph("📋 Workflow-Informationen", self.styles['CustomSubtitle']))
        
        workflow_info = [
            ["Query:", workflow_data.get('query', 'N/A')],
            ["Demo ID:", workflow_data.get('demoId', 'N/A')],
            ["Gestartet:", workflow_data.get('started_at', 'N/A')],
            ["Abgeschlossen:", workflow_data.get('completed_at', 'N/A')],
            ["Status:", workflow_data.get('status', 'N/A')]
        ]
        
        workflow_table = Table(workflow_info, colWidths=[2*inch, 4*inch])
        workflow_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (0, -1), HexColor('#374151')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(workflow_table)
        story.append(Spacer(1, 20))
        
        # Workflow Status
        story.append(Paragraph("🔄 Agenten-Status", self.styles['CustomSubtitle']))
        
        workflow_status = workflow_data.get('workflow_status', {})
        status_data = [
            ["Agent", "Status"],
            ["🎯 Orchestrator", workflow_status.get('orchestrator', 'unknown')],
            ["📊 Datenanalyse-Agent", workflow_status.get('dataAnalyst', 'unknown')],
            ["🔧 DuckDB Tool", workflow_status.get('duckdbTool', 'unknown')],
            ["📝 Bericht-Generator", workflow_status.get('reportGenerator', 'unknown')]
        ]
        
        status_table = Table(status_data, colWidths=[3*inch, 2*inch])
        status_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(status_table)
        story.append(Spacer(1, 30))
        
        # Echte Analyse-Ergebnisse aus dem LangGraph-Workflow verwenden
        story.append(Paragraph("📊 Analyseergebnis", self.styles['CustomSubtitle']))
        
        # Echten Bericht aus workflow_data extrahieren
        final_output = workflow_data.get('final_result', '')
        if not final_output:
            # Fallback: Versuche andere Felder
            final_output = workflow_data.get('final_output', '')
        if not final_output:
            final_output = "Keine Analyseergebnisse verfügbar. Workflow-Daten: " + str(list(workflow_data.keys()))
        
        # Bericht-Text formatieren und in PDF einfügen
        # Sichere Formatierung für ReportLab
        import re
        
        # Entferne/ersetze problematische Zeichen
        formatted_output = final_output.replace('\\U0001f4ca', '📊')
        formatted_output = formatted_output.replace('\\U0001f3af', '🎯')
        formatted_output = formatted_output.replace('\\U0001f4c8', '📈')
        formatted_output = formatted_output.replace('\\U0001f4dd', '📝')
        formatted_output = formatted_output.replace('\\xe4', 'ä')
        formatted_output = formatted_output.replace('\\xf6', 'ö')
        formatted_output = formatted_output.replace('\\xfc', 'ü')
        formatted_output = formatted_output.replace('\\xdf', 'ß')
        
        # Markdown **bold** korrekt zu HTML konvertieren
        formatted_output = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', formatted_output)
        
        # Zeilenumbrüche
        formatted_output = formatted_output.replace('\n\n', '<br/><br/>')
        formatted_output = formatted_output.replace('\n', '<br/>')
        
        # Entferne HTML-Tabellen (nicht unterstützt von ReportLab)
        formatted_output = re.sub(r'\|.*?\|', '', formatted_output)
        formatted_output = re.sub(r'-+\s*\|\s*-+', '', formatted_output)
        
        story.append(Paragraph(formatted_output, self.styles['CustomBody']))
        story.append(Spacer(1, 20))
        
        # Zusätzliche Informationen nur wenn verfügbar
        analysis_result = workflow_data.get('analysis_result', {})
        if analysis_result:
            story.append(Paragraph("📈 Zusätzliche Details", self.styles['CustomSubtitle']))
            details_text = f"Analyse-Status: {analysis_result.get('status', 'Unbekannt')}"
            story.append(Paragraph(details_text, self.styles['CustomBody']))
            story.append(Spacer(1, 10))
        
        # Footer
        story.append(Spacer(1, 30))
        footer_text = f"""
        <i>Generiert am {datetime.now().strftime('%d.%m.%Y um %H:%M')} Uhr durch das 
        LangGraph Multi-Agenten System</i>
        """
        story.append(Paragraph(footer_text, self.styles['Normal']))
        
        # PDF erstellen
        doc.build(story)
        return output_path
    
    def create_reports_directory(self) -> str:
        """Erstellt das Reports-Verzeichnis falls es nicht existiert"""
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        return reports_dir 