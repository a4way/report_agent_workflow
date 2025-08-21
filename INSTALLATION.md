# 🚀 Installation & Setup

## Schnellstart

1. **Dependencies installieren**:
```bash
pip install -r requirements.txt
```

2. **OpenAI API Key konfigurieren**:
```bash
# Erstelle .env Datei
echo "OPENAI_API_KEY=your_actual_api_key_here" > .env
```

3. **System testen**:
```bash
python test_system.py
```

4. **Anwendung starten**:
```bash
python main.py
```

## Detaillierte Installation

### Voraussetzungen
- Python 3.8+
- OpenAI API Key
- Mindestens 100MB freier Speicherplatz

### Schritt-für-Schritt

1. **Repository Setup**:
```bash
cd langgraph_agent_visualization
```

2. **Virtuelle Umgebung (empfohlen)**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate     # Windows
```

3. **Dependencies installieren**:
```bash
pip install -r requirements.txt
```

4. **OpenAI API Key einrichten**:
   - Gehe zu https://platform.openai.com/api-keys
   - Erstelle einen neuen API Key
   - Füge ihn in `.env` ein:
   ```bash
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

5. **System validieren**:
```bash
python test_system.py
```

### Erste Verwendung

1. **Demo ausführen**:
```bash
python main.py --demo
```

2. **Interaktiv verwenden**:
```bash
python main.py
```

### Beispiel-Anfragen

- "Analysiere den Umsatz nach Akquisitionskanälen"
- "Wie ist die Performance unserer Marketing-Kampagnen?"
- "Zeige mir die wichtigsten KPIs für das E-Commerce Business"

## Troubleshooting

### Häufige Probleme

**ImportError bei langchain/langgraph**:
```bash
pip install --upgrade langchain langgraph langchain-openai
```

**DuckDB Fehler**:
```bash
pip install --upgrade duckdb pandas
```

**OpenAI API Fehler**:
- Überprüfe API Key in `.env`
- Stelle sicher, dass du Guthaben auf deinem OpenAI Account hast
- Verwende einen gültigen API Key (beginnt mit `sk-`)

**CSV-Dateien nicht gefunden**:
- Stelle sicher, dass der `show_case_data/` Ordner existiert
- Alle CSV-Dateien müssen vorhanden sein

### Support

Bei weiteren Problemen:
1. Führe `python test_system.py` aus
2. Überprüfe die Fehlermeldungen
3. Stelle sicher, dass alle Dependencies installiert sind

## Performance-Tipps

- Verwende `gpt-4o-mini` für kostengünstige Demos
- Upgrade zu `gpt-4o` für bessere Analyse-Qualität
- Die erste Anfrage dauert länger (Modell-Initialisierung)

---

*Bei erfolgreicher Installation sollten alle Tests grün sein! 🎉* 