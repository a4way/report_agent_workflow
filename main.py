#!/usr/bin/env python3
"""
LangGraph Multi-Agenten Showcase
Hauptanwendung für E-Commerce Datenanalyse
"""
import sys
import os
from orchestrator import MultiAgentOrchestrator


def main():
    """Hauptfunktion für die CLI-Anwendung"""
    
    print("🤖 LangGraph Multi-Agenten E-Commerce Analyse")
    print("=" * 50)
    
    # Prüfe ob .env existiert
    if not os.path.exists('.env'):
        print("❌ Bitte erstelle eine .env Datei mit deinem OPENAI_API_KEY")
        print("   Kopiere .env.example zu .env und füge deinen API Key hinzu")
        return
    
    # Orchestrator initialisieren
    try:
        orchestrator = MultiAgentOrchestrator()
        print("✅ Multi-Agenten-System erfolgreich initialisiert")
    except Exception as e:
        print(f"❌ Fehler beim Initialisieren: {e}")
        return
    
    print("\n📋 Beispiel-Anfragen:")
    print("• 'Analysiere den Umsatz nach Akquisitionskanälen'")
    print("• 'Wie ist die Performance unserer Marketing-Kampagnen?'")
    print("• 'Zeige mir die wichtigsten KPIs für das E-Commerce Business'")
    print("• 'Welche Produkte haben die beste Marge?'")
    print("• 'Wie entwickelt sich unser AOV über die Zeit?'")
    
    while True:
        print("\n" + "─" * 50)
        user_input = input("🎯 Ihre Analyse-Anfrage (oder 'exit' zum Beenden): ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("👋 Auf Wiedersehen!")
            break
        
        if not user_input:
            print("⚠️  Bitte geben Sie eine Anfrage ein")
            continue
        
        print(f"\n🔄 Verarbeite Anfrage: {user_input}")
        print("⏳ Dies kann einen Moment dauern...\n")
        
        try:
            # Anfrage durch Multi-Agenten-System verarbeiten
            result = orchestrator.process_request(user_input)
            
            print("\n" + "=" * 60)
            print(result)
            print("=" * 60)
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Verarbeitung abgebrochen")
            continue
        except Exception as e:
            print(f"\n❌ Fehler bei der Verarbeitung: {e}")


def run_demo():
    """Führt eine Demo mit vordefinierten Anfragen aus"""
    
    print("🎬 Demo-Modus: LangGraph Multi-Agenten System")
    print("=" * 50)
    
    try:
        orchestrator = MultiAgentOrchestrator()
    except Exception as e:
        print(f"❌ Fehler beim Initialisieren: {e}")
        return
    
    demo_requests = [
        "Analysiere den Gesamtumsatz und AOV für unser E-Commerce Business",
        "Wie performt jeder Akquisitionskanal in Bezug auf Umsatz und Anzahl Bestellungen?",
        "Berechne die Gross Margin für unser Produktportfolio"
    ]
    
    for i, request in enumerate(demo_requests, 1):
        print(f"\n🎯 Demo {i}/3: {request}")
        print("⏳ Verarbeitung läuft...\n")
        
        try:
            result = orchestrator.process_request(request)
            print("=" * 60)
            print(result)
            print("=" * 60)
            
            if i < len(demo_requests):
                input("\n⏸️  Drücke Enter für die nächste Demo...")
                
        except Exception as e:
            print(f"❌ Fehler bei Demo {i}: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo()
    else:
        main() 