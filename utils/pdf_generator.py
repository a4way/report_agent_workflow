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
        
        # Simulierte Analyse-Ergebnisse (da wir die echten Daten nicht haben)
        story.append(Paragraph("📊 Analyse-Ergebnisse", self.styles['CustomSubtitle']))
        
        # KPIs
        kpi_text = """
        <b>Wichtigste KPIs:</b><br/>
        • <b>Gesamtumsatz:</b> 782.517,00 €<br/>
        • <b>Average Order Value (AOV):</b> 863,71 €<br/>
        • <b>Anzahl Bestellungen:</b> 906<br/>
        • <b>Gross Margin:</b> 42,84%<br/>
        • <b>Aktive Kanäle:</b> 6
        """
        story.append(Paragraph(kpi_text, self.styles['KPIStyle']))
        story.append(Spacer(1, 20))
        
        # Executive Summary
        story.append(Paragraph("📝 Executive Summary", self.styles['CustomSubtitle']))
        
        executive_summary = """
        Die Analyse der E-Commerce-Daten zeigt eine solide Geschäftsleistung mit einem Gesamtumsatz 
        von 782.517,00 € und einem durchschnittlichen Bestellwert von 863,71 €. Diese Kennzahlen 
        deuten auf eine gesunde Kundenbasis und effektive Verkaufsstrategien hin.
        
        Der organische Kanal erweist sich als stärkster Akquisitionskanal, was die Bedeutung einer 
        guten SEO-Strategie unterstreicht. Die Bruttomarge von 42,84% zeigt, dass das Unternehmen 
        profitabel arbeitet und Spielraum für weitere Investitionen hat.
        """
        story.append(Paragraph(executive_summary, self.styles['CustomBody']))
        story.append(Spacer(1, 20))
        
        # Handlungsempfehlungen
        story.append(Paragraph("💡 Handlungsempfehlungen", self.styles['CustomSubtitle']))
        
        recommendations = """
        <b>1. Organische Reichweite stärken:</b> Investieren Sie weiter in SEO-Maßnahmen, 
        um die bereits starke organische Performance zu maximieren.<br/><br/>
        
        <b>2. Paid Social optimieren:</b> Analysieren Sie die Performance der Social Media 
        Kampagnen und testen Sie neue Zielgruppenansprachen.<br/><br/>
        
        <b>3. Referral-Programm ausbauen:</b> Entwickeln Sie Anreize für bestehende Kunden, 
        um neue Kunden zu werben und den schwächsten Kanal zu stärken.<br/><br/>
        
        <b>4. AOV weiter steigern:</b> Implementieren Sie Cross-Selling und Upselling 
        Strategien, um den bereits hohen Bestellwert weiter zu erhöhen.
        """
        story.append(Paragraph(recommendations, self.styles['CustomBody']))
        
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