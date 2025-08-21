# 🤖 LangGraph Multi-Agenten E-Commerce Analyse

Ein fortschrittlicher Multi-Agenten-Workflow basierend auf LangGraph für die Analyse von E-Commerce-Daten. Das System verwendet OpenAI GPT-4 und DuckDB für intelligente Datenanalyse und Berichtserstellung.

## 🏗️ Architektur

### Multi-Agenten-System
1. **🎯 Orchestrator**: Koordiniert den gesamten Workflow und verteilt Anfragen
2. **🔧 DuckDB-Tool**: Führt SQL-Queries auf lokale CSV-Dateien aus  
3. **📊 Datenanalyse-Agent**: Analysiert Daten und berechnet KPIs
4. **📝 Bericht-Generator-Agent**: Erstellt professionelle Fließtext-Berichte

### Workflow
```
Benutzer-Anfrage → Orchestrator → Datenanalyse → Berichtserstellung → Finaler Output
```

## 📊 Verfügbare Daten

Das System arbeitet mit realistischen E-Commerce-Daten:
- **customers.csv**: Kundendaten mit Akquisitionskanälen
- **orders.csv**: Bestellungen mit Status und Zahlungsarten
- **order_items.csv**: Bestellpositionen mit Preisen und Rabatten
- **products.csv**: Produktkatalog mit Kosten und Preisen
- **marketing_spend.csv**: Marketing-Ausgaben nach Kanälen
- **web_analytics_daily.csv**: Tägliche Web-Analytics-Daten

## 🚀 Installation

1. **Repository klonen**:
```bash
git clone <repository-url>
cd langgraph_agent_visualization
```

2. **Dependencies installieren**:
```bash
pip install -r requirements.txt
```

3. **Umgebungsvariablen konfigurieren**:
```bash
cp .env.example .env
# Füge deinen OpenAI API Key in .env hinzu
```

4. **Anwendung starten**:
```bash
python main.py
```

## 💡 Verwendung

### Interaktiver Modus
```bash
python main.py
```

### Demo-Modus
```bash
python main.py --demo
```

### Beispiel-Anfragen
- "Analysiere den Umsatz nach Akquisitionskanälen"
- "Wie ist die Performance unserer Marketing-Kampagnen?"
- "Zeige mir die wichtigsten KPIs für das E-Commerce Business"
- "Welche Produkte haben die beste Marge?"
- "Wie entwickelt sich unser AOV über die Zeit?"

## 📈 Unterstützte KPIs

- **Revenue**: Gesamtumsatz aus bezahlten Bestellungen
- **AOV (Average Order Value)**: Durchschnittlicher Bestellwert
- **Conversion Rate**: Verhältnis Transaktionen zu Sessions
- **ROAS (Return on Ad Spend)**: Marketing-ROI nach Kanälen
- **CAC (Customer Acquisition Cost)**: Kundenakquisitionskosten
- **Gross Margin**: Bruttogewinnspanne

## 🔧 Technische Details

### Verwendete Technologien
- **LangGraph**: Orchestrierung des Multi-Agenten-Workflows
- **OpenAI GPT-4**: Large Language Model für Analyse und Berichtserstellung
- **DuckDB**: In-Memory SQL-Engine für CSV-Datenanalyse
- **LangChain**: Framework für LLM-Integration
- **Pandas**: Datenmanipulation

### Projektstruktur
```
langgraph_agent_visualization/
├── agents/                     # Agent-Implementierungen
│   ├── data_analyst_agent.py   # Datenanalyse-Agent
│   └── report_generator_agent.py # Bericht-Generator
├── tools/                      # Tools und Utilities
│   └── duckdb_tool.py         # DuckDB SQL-Tool
├── show_case_data/            # CSV-Dateien
├── orchestrator.py            # Haupt-Orchestrator
├── config.py                  # Konfiguration
├── main.py                    # CLI-Anwendung
└── requirements.txt           # Dependencies
```

## 🎯 Features

### Intelligente Anfrageverarbeitung
- Automatische Klassifizierung von Business-Anfragen
- Kontextbewusste KPI-Auswahl
- Strukturierte Datenanalyse

### Professionelle Berichtserstellung
- Executive Summaries
- Handlungsempfehlungen
- Trend-Analyse
- Konkrete Zahlen und Insights

### Skalierbare Architektur
- Modulare Agent-Struktur
- Erweiterbare Tool-Integration
- Flexible Workflow-Konfiguration

## 🛠️ Entwicklung

### Neue Agenten hinzufügen
1. Erstelle eine neue Klasse in `agents/`
2. Implementiere die benötigten Methoden
3. Registriere den Agenten im Orchestrator

### Neue Tools hinzufügen
1. Erstelle ein neues Tool in `tools/`
2. Erbe von `BaseTool` (LangChain)
3. Implementiere `_run()` und `_arun()` Methoden

### Workflow erweitern
1. Füge neue Knoten im `_create_workflow()` hinzu
2. Definiere Edges zwischen den Knoten
3. Erweitere die `WorkflowState` wenn nötig

## 📝 Lizenz

MIT License - siehe LICENSE-Datei für Details.

## 🤝 Beiträge

Beiträge sind willkommen! Bitte erstelle einen Pull Request mit deinen Änderungen.

## 📞 Support

Bei Fragen oder Problemen erstelle bitte ein Issue im Repository.

---

*Entwickelt mit ❤️ und LangGraph für intelligente E-Commerce-Analyse* 