#!/usr/bin/env python3
"""
Test-Script für das LangGraph Multi-Agenten System
"""
import os
import sys
from tools.duckdb_tool import DuckDBQueryTool


def test_duckdb_tool():
    """Testet das DuckDB Tool mit einer einfachen Query"""
    print("🧪 Teste DuckDB Tool...")
    
    tool = DuckDBQueryTool()
    
    # Test Query: Anzahl Kunden
    test_query = "SELECT COUNT(*) as customer_count FROM customers"
    result = tool._run(test_query)
    
    print(f"✅ Query-Ergebnis: {result}")
    return "customer_count" in result


def test_csv_files():
    """Überprüft ob alle CSV-Dateien vorhanden sind"""
    print("📁 Überprüfe CSV-Dateien...")
    
    required_files = [
        "show_case_data/customers.csv",
        "show_case_data/orders.csv", 
        "show_case_data/order_items.csv",
        "show_case_data/products.csv",
        "show_case_data/marketing_spend.csv",
        "show_case_data/web_analytics_daily.csv"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Fehlende Dateien: {missing_files}")
        return False
    else:
        print("✅ Alle CSV-Dateien gefunden")
        return True


def test_imports():
    """Testet ob alle wichtigen Module importiert werden können"""
    print("📦 Teste Imports...")
    
    try:
        from config import CSV_FILES, LLM_MODEL
        print("✅ Config importiert")
        
        from tools.duckdb_tool import DuckDBQueryTool
        print("✅ DuckDB Tool importiert")
        
        from agents.data_analyst_agent import DataAnalystAgent
        print("✅ DataAnalyst Agent importiert")
        
        from agents.report_generator_agent import ReportGeneratorAgent  
        print("✅ ReportGenerator Agent importiert")
        
        from orchestrator import MultiAgentOrchestrator
        print("✅ Orchestrator importiert")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import-Fehler: {e}")
        return False


def main():
    """Führt alle Tests aus"""
    print("🚀 LangGraph Multi-Agenten System - Systemtest")
    print("=" * 50)
    
    tests = [
        ("CSV-Dateien", test_csv_files),
        ("Imports", test_imports),
        ("DuckDB Tool", test_duckdb_tool)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Test: {test_name}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: BESTANDEN")
            else:
                print(f"❌ {test_name}: FEHLGESCHLAGEN")
        except Exception as e:
            print(f"❌ {test_name}: FEHLER - {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Testergebnisse: {passed}/{total} Tests bestanden")
    
    if passed == total:
        print("🎉 Alle Tests erfolgreich! Das System ist bereit.")
        print("\nNächste Schritte:")
        print("1. Füge deinen OpenAI API Key in .env hinzu")
        print("2. Starte das System mit: python main.py")
    else:
        print("⚠️  Einige Tests sind fehlgeschlagen. Bitte überprüfe die Konfiguration.")


if __name__ == "__main__":
    main() 