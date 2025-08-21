#!/usr/bin/env python3
"""
Starter-Script für das komplette LangGraph Multi-Agenten System
Startet Backend-API und Frontend gleichzeitig
"""
import os
import sys
import subprocess
import time
import signal
from pathlib import Path

def check_dependencies():
    """Überprüft ob alle Dependencies installiert sind"""
    print("🔍 Überprüfe Dependencies...")
    
    # Check Python dependencies
    try:
        import fastapi
        import uvicorn
        import langgraph
        print("✅ Python Dependencies installiert")
    except ImportError as e:
        print(f"❌ Fehlende Python Dependency: {e}")
        print("💡 Führe aus: pip install -r requirements.txt")
        return False
    
    # Check if Node.js is available
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js verfügbar: {result.stdout.strip()}")
        else:
            print("❌ Node.js nicht gefunden")
            return False
    except FileNotFoundError:
        print("❌ Node.js nicht installiert")
        print("💡 Installiere Node.js von https://nodejs.org/")
        return False
    
    return True

def setup_frontend():
    """Setup und Installation des Frontends"""
    frontend_path = Path("frontend")
    
    if not frontend_path.exists():
        print("❌ Frontend-Verzeichnis nicht gefunden")
        return False
    
    print("📦 Installiere Frontend Dependencies...")
    os.chdir(frontend_path)
    
    # Install npm dependencies
    result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ npm install fehlgeschlagen: {result.stderr}")
        return False
    
    print("✅ Frontend Dependencies installiert")
    os.chdir("..")
    return True

def start_backend():
    """Startet das FastAPI Backend"""
    print("🚀 Starte Backend-API...")
    
    backend_process = subprocess.Popen([
        sys.executable, "web_api.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Wait a bit for backend to start
    time.sleep(3)
    
    if backend_process.poll() is None:
        print("✅ Backend-API läuft auf http://localhost:8000")
        return backend_process
    else:
        stdout, stderr = backend_process.communicate()
        print(f"❌ Backend-Start fehlgeschlagen:")
        print(f"STDOUT: {stdout}")
        print(f"STDERR: {stderr}")
        return None

def start_frontend():
    """Startet das React Frontend"""
    print("🎨 Starte React Frontend...")
    
    frontend_process = subprocess.Popen([
        'npm', 'start'
    ], cwd='frontend', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Wait a bit for frontend to start
    time.sleep(5)
    
    if frontend_process.poll() is None:
        print("✅ React Frontend läuft auf http://localhost:3000")
        return frontend_process
    else:
        stdout, stderr = frontend_process.communicate()
        print(f"❌ Frontend-Start fehlgeschlagen:")
        print(f"STDOUT: {stdout}")
        print(f"STDERR: {stderr}")
        return None

def main():
    """Hauptfunktion"""
    print("🤖 LangGraph Multi-Agenten System Starter")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup frontend if needed
    if not Path("frontend/node_modules").exists():
        if not setup_frontend():
            sys.exit(1)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        sys.exit(1)
    
    # Start frontend  
    frontend_process = start_frontend()
    if not frontend_process:
        backend_process.terminate()
        sys.exit(1)
    
    print("\n🎉 System erfolgreich gestartet!")
    print("📊 Frontend Dashboard: http://localhost:3000")
    print("🔧 Backend API: http://localhost:8000")
    print("📋 API Dokumentation: http://localhost:8000/api/docs")
    print("\n⌨️  Drücke Ctrl+C zum Beenden")
    
    # Handle shutdown
    def signal_handler(sig, frame):
        print("\n🛑 Beende System...")
        if frontend_process:
            frontend_process.terminate()
        if backend_process:
            backend_process.terminate()
        print("👋 System beendet")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Wait for processes
    try:
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("❌ Backend-Prozess beendet")
                break
            
            if frontend_process.poll() is not None:
                print("❌ Frontend-Prozess beendet")
                break
                
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main() 