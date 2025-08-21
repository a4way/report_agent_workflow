import React, { useCallback } from 'react';
import { createPortal } from 'react-dom';
import WorkflowGraph from './components/WorkflowGraph';
import DemoSelector from './components/DemoSelector';
import LogPanel from './components/LogPanel';
import { useWorkflowState } from './hooks/useWorkflowState';
import { Bot, Github, ExternalLink } from 'lucide-react';
import './index.css';

function App() {
  const {
    workflowStatus,
    currentStep,
    logs,
    isRunning,
    currentWorkflowId,
    finalResult,
    startDemo,
    clearLogs
  } = useWorkflowState();

  const handleStartDemo = useCallback((query, demoId) => {
    startDemo(query, demoId);
  }, [startDemo]);

  return (
    <>
      {/* Fixed Current Step Overlay - Portal für echtes fixed positioning */}
      {isRunning && currentStep && createPortal(
        <div className="fixed top-20 left-1/2 transform -translate-x-1/2 z-[9999] bg-white rounded-lg shadow-2xl border-2 border-blue-200 p-4 min-w-96 max-w-lg">
          <div className="flex items-center gap-3">
            <div className="w-4 h-4 bg-blue-500 rounded-full animate-pulse"></div>
            <div>
              <h4 className="font-semibold text-gray-900 text-sm">⏱️ Aktueller Schritt:</h4>
              <span className="text-gray-800 text-sm">{currentStep}</span>
            </div>
          </div>
        </div>,
        document.body
      )}
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg">
                <Bot className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gradient">
                  LangGraph Multi-Agenten Dashboard
                </h1>
                <p className="text-sm text-gray-600">
                  Interaktive Visualisierung für AI-Agenten Workflows
                </p>
                <p className="text-xs text-gray-400 mt-1">
                  by Dr. Henrik Kortum-Landwehr
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <a
                href="https://github.com/a4way/report_agent_workflow"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <Github className="w-4 h-4" />
                <span className="hidden sm:inline">GitHub</span>
                <ExternalLink className="w-3 h-3" />
              </a>
              
              <div className="flex items-center gap-2 px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span>System Online</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content - Vertical Layout */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8">
          
          {/* Demo Selector Section */}
          <section className="bg-white rounded-lg shadow-lg border border-gray-200">
            <div className="p-6">
              <DemoSelector 
                onStartDemo={handleStartDemo}
                isRunning={isRunning}
              />
            </div>
          </section>

          {/* System Status */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-200">
              <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                🚀 System Status
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Aktive Agenten:</span>
                  <span className="font-medium">
                    {Object.values(workflowStatus).filter(status => status === 'active').length}/4
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Log Einträge:</span>
                  <span className="font-medium">{logs.length}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Workflow Status:</span>
                  <span className={`font-medium ${isRunning ? 'text-blue-600' : 'text-gray-500'}`}>
                    {isRunning ? 'Aktiv' : 'Bereit'}
                  </span>
                </div>
              </div>
            </div>
            
            {/* Current Step Indicator */}
            <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-200 md:col-span-2">
              <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                ⏱️ Aktueller Status
              </h3>
              {currentStep ? (
                <div className="flex items-center gap-3">
                  <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
                  <span className="text-gray-800">{currentStep}</span>
                </div>
              ) : (
                <div className="flex items-center gap-3">
                  <div className="w-3 h-3 bg-gray-300 rounded-full"></div>
                  <span className="text-gray-500">System bereit - Wähle einen Demo Case</span>
                </div>
              )}
            </div>
          </div>

          {/* Workflow Graph Section */}
          <section className="bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden">
            <div className="p-4 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-purple-50">
              <h2 className="text-xl font-semibold text-gray-900 flex items-center gap-2">
                🔄 Workflow Visualisierung
              </h2>
              <p className="text-sm text-gray-600 mt-1">
                Live-Tracking des Multi-Agenten-Workflows
              </p>
            </div>
            <div className="h-80">
              <WorkflowGraph 
                workflowStatus={workflowStatus}
                currentStep={currentStep}
              />
            </div>
          </section>

          {/* Results Section */}
          {logs.some(log => log.level === 'success' && log.message.includes('Workflow erfolgreich')) && (
            <section className="bg-white rounded-lg shadow-lg border border-gray-200">
              <div className="p-6 border-b border-gray-200 bg-gradient-to-r from-green-50 to-blue-50">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-xl font-semibold text-gray-900 mb-2 flex items-center gap-2">
                      📊 Analyseergebnisse
                    </h2>
                    <p className="text-sm text-gray-600">Generierter Bericht des Multi-Agenten-Systems</p>
                  </div>
                  
                  {/* PDF Download Button */}
                  <button
                    onClick={async () => {
                      try {
                        console.log('🔍 Current Workflow ID:', currentWorkflowId);
                        
                        if (currentWorkflowId) {
                          const downloadUrl = `/api/workflow/${currentWorkflowId}/report/download`;
                          console.log('🔍 Download URL:', downloadUrl);
                          
                          const response = await fetch(downloadUrl);
                          console.log('🔍 Response status:', response.status);
                          console.log('🔍 Response headers:', [...response.headers.entries()]);
                          
                          if (response.ok) {
                            const blob = await response.blob();
                            console.log('🔍 Blob size:', blob.size, 'bytes');
                            
                            const url = window.URL.createObjectURL(blob);
                            const a = document.createElement('a');
                            a.href = url;
                            a.download = `langgraph_report_${Date.now()}.pdf`;
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                            window.URL.revokeObjectURL(url);
                          } else {
                            const errorText = await response.text();
                            console.error('🔍 Error response:', errorText);
                            alert(`PDF konnte nicht heruntergeladen werden. Status: ${response.status}\nFehler: ${errorText}`);
                          }
                        } else {
                          alert('Kein aktiver Workflow gefunden. Starte erst eine Demo-Analyse.');
                        }
                      } catch (error) {
                        console.error('🔍 Fehler beim Download:', error);
                        alert('Fehler beim Download: ' + error.message);
                      }
                    }}
                    className="flex items-center gap-2 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors text-sm"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    PDF-Bericht herunterladen
                  </button>
                </div>
              </div>
              
              <div className="p-6">
                <div className="bg-gray-50 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">📈 Analyseergebnis</h3>
                  <div className="prose prose-sm max-w-none text-gray-700">
                    {finalResult ? (
                      <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
                        <div className="prose prose-sm max-w-none">
                          <div 
                            className="text-gray-800 leading-relaxed"
                            dangerouslySetInnerHTML={{
                              __html: finalResult
                                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                                .replace(/\n\n/g, '</p><p class="mb-4">')
                                .replace(/\n/g, '<br>')
                                .replace(/^(.*)$/, '<p class="mb-4">$1</p>')
                                .replace(/(\d+\.\s)/g, '<br><strong>$1</strong>')
                                .replace(/(-\s)/g, '<br>• ')
                            }}
                          />
                        </div>
                        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-4">
                          <p className="text-sm text-blue-800">
                            <strong>🤖 Automatisch generiert</strong> durch das LangGraph Multi-Agenten-System am {new Date().toLocaleDateString('de-DE')} um {new Date().toLocaleTimeString('de-DE')} Uhr
                          </p>
                        </div>
                      </div>
                    ) : (
                      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                        <p className="text-yellow-800">
                          <strong>⏳ Warten auf Analyseergebnis...</strong> Das LangGraph-System verarbeitet gerade die Daten.
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </section>
          )}

          {/* Logs Section */}
          <section>
            <LogPanel 
              logs={logs}
              onClearLogs={clearLogs}
            />
          </section>
        </div>


      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-sm text-gray-500">
            <p>
              🤖 Powered by <strong>LangGraph</strong>, <strong>OpenAI GPT-4</strong> & <strong>React</strong>
            </p>
            <p className="mt-1">
              Multi-Agenten System für intelligente E-Commerce Datenanalyse
            </p>
            <p className="mt-2 text-xs text-gray-400">
              by Dr. Henrik Kortum-Landwehr
            </p>
          </div>
        </div>
      </footer>
    </div>
    </>
  );
}

export default App; 