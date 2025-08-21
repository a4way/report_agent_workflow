# 🤖 LangGraph Multi-Agenten Frontend

Ein modernes React-Frontend zur Visualisierung und Steuerung des LangGraph Multi-Agenten-Workflows.

## ✨ Features

- **🔄 Live Workflow-Visualisierung** mit React Flow
- **🎬 Interaktive Demo Cases** zum Starten von Analysen  
- **📊 Echtzeit-Logging** mit detaillierten Workflow-Informationen
- **🎨 Moderne UI** mit Tailwind CSS und Lucide Icons
- **📱 Responsive Design** für Desktop und Mobile
- **⚡ Live-Updates** des Workflow-Status

## 🚀 Installation & Start

### Voraussetzungen
- Node.js 16+ 
- npm oder yarn

### Setup
```bash
cd frontend
npm install
npm start
```

Das Frontend startet auf `http://localhost:3000` und verbindet sich automatisch mit der Backend-API auf Port 8000.

## 🏗️ Architektur

### Komponenten
- **App.jsx** - Hauptkomponente mit Layout
- **WorkflowGraph.jsx** - Interaktive Workflow-Visualisierung
- **DemoCases.jsx** - Demo-Case-Auswahl und -steuerung
- **LogPanel.jsx** - Live-Logging mit Export-Funktion

### Hooks
- **useWorkflowState.js** - State Management für Workflows

### Styling
- **Tailwind CSS** - Utility-First CSS Framework
- **Custom Components** - Vordefinierte Workflow-Komponenten
- **Responsive Design** - Mobile-First Approach

## 🎯 Verwendung

1. **Demo Case auswählen** - Wähle eine der 3 vorkonfigurierten Analysen
2. **Workflow starten** - Klicke auf "Demo starten" 
3. **Live-Tracking** - Verfolge den Fortschritt im Workflow-Graph
4. **Logs überwachen** - Sieh detaillierte Informationen im Log-Panel
5. **Ergebnisse anzeigen** - Betrachte die finalen Analyseergebnisse

## 🔧 Entwicklung

### Scripts
```bash
npm start          # Entwicklungsserver
npm run build      # Produktions-Build
npm test           # Tests ausführen
npm run eject      # React-Konfiguration anpassen
```

### Anpassungen
- Neue Demo Cases in `DemoCases.jsx` hinzufügen
- Workflow-Knoten in `WorkflowGraph.jsx` erweitern
- Styling in `tailwind.config.js` anpassen

## 📦 Dependencies

### Haupt-Dependencies
- **React 18** - UI Framework
- **React Flow** - Workflow-Visualisierung
- **Tailwind CSS** - Styling
- **Lucide React** - Icons
- **Axios** - HTTP Client

### Dev-Dependencies
- **React Scripts** - Build-Tools
- **PostCSS** - CSS-Processing
- **Autoprefixer** - CSS-Vendor-Prefixes

## 🌐 API Integration

Das Frontend kommuniziert mit der FastAPI-Backend über:
- `POST /api/workflow/start` - Workflow starten
- `GET /api/workflow/{id}/status` - Status abrufen  
- `GET /api/workflow/{id}/logs` - Logs abrufen

## 🎨 Design System

### Farben
- **Primary**: Blau-Töne für Haupt-UI-Elemente
- **Success**: Grün für erfolgreiche Aktionen
- **Warning**: Gelb für Warnungen
- **Error**: Rot für Fehler

### Animationen
- **Pulse**: Für aktive Zustände
- **Spin**: Für Lade-Indikatoren
- **Bounce**: Für Aufmerksamkeit
- **Glow**: Für Hover-Effekte

---

*Entwickelt mit ❤️ und React für die LangGraph Multi-Agenten Visualisierung* 