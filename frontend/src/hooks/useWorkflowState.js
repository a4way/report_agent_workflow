import { useState, useCallback, useRef } from 'react';
import axios from 'axios';

export const useWorkflowState = () => {
  const [workflowStatus, setWorkflowStatus] = useState({
    orchestrator: 'idle',
    dataAnalyst: 'idle',
    duckdbTool: 'idle',
    reportGenerator: 'idle'
  });
  
  const [currentStep, setCurrentStep] = useState('');
  const [logs, setLogs] = useState([]);
  const [isRunning, setIsRunning] = useState(false);
  const [currentWorkflowId, setCurrentWorkflowId] = useState(null);
  const abortControllerRef = useRef(null);

  const addLog = useCallback((level, message, agent = null, details = null) => {
    const logEntry = {
      timestamp: Date.now(),
      level,
      message,
      agent,
      details
    };
    
    setLogs(prevLogs => [...prevLogs, logEntry]);
  }, []);

  const updateWorkflowStatus = useCallback((agent, status) => {
    setWorkflowStatus(prev => ({
      ...prev,
      [agent]: status
    }));
  }, []);

  const simulateWorkflowProgress = useCallback(async (query, demoId) => {
    // Reset state
    setWorkflowStatus({
      orchestrator: 'idle',
      dataAnalyst: 'idle', 
      duckdbTool: 'idle',
      reportGenerator: 'idle'
    });
    
    setCurrentStep('');
    setIsRunning(true);
    
    addLog('info', `🚀 Starte Demo: ${demoId}`, 'System');
    addLog('info', `📝 Query: "${query}"`, 'System');

    try {
      // Step 1: Orchestrator starts
      setCurrentStep('Orchestrator initialisiert Workflow...');
      updateWorkflowStatus('orchestrator', 'active');
      addLog('info', '🎯 Orchestrator: Anfrage wird klassifiziert', 'Orchestrator');
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      updateWorkflowStatus('orchestrator', 'completed');
      addLog('success', '✅ Orchestrator: Anfrage erfolgreich klassifiziert', 'Orchestrator');

      // Step 2: Data Analyst starts
      setCurrentStep('Datenanalyse-Agent startet Analyse...');
      updateWorkflowStatus('dataAnalyst', 'active');
      addLog('info', '📊 Datenanalyse-Agent: Beginne mit der Datenanalyse', 'DataAnalyst');
      await new Promise(resolve => setTimeout(resolve, 1500));

      // Step 3: DuckDB Tool executes queries
      setCurrentStep('DuckDB Tool führt SQL-Queries aus...');
      updateWorkflowStatus('duckdbTool', 'active');
      addLog('info', '🔧 DuckDB Tool: Führe SQL-Queries auf CSV-Daten aus', 'DuckDBTool');
      
      // Simulate multiple queries
      const queries = [
        'SELECT SUM(revenue) FROM orders WHERE status = "paid"',
        'SELECT channel, COUNT(*) FROM customers GROUP BY channel',
        'SELECT AVG(order_value) FROM order_items'
      ];
      
      for (const query of queries) {
        addLog('info', `🔍 SQL Query: ${query}`, 'DuckDBTool');
        await new Promise(resolve => setTimeout(resolve, 800));
      }
      
      updateWorkflowStatus('duckdbTool', 'completed');
      addLog('success', '✅ DuckDB Tool: Alle Queries erfolgreich ausgeführt', 'DuckDBTool');

      // Step 4: Data Analyst completes analysis
      setCurrentStep('Datenanalyse-Agent berechnet KPIs...');
      addLog('info', '📈 Datenanalyse-Agent: Berechne KPIs und erstelle Insights', 'DataAnalyst');
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      updateWorkflowStatus('dataAnalyst', 'completed');
      addLog('success', '✅ Datenanalyse-Agent: KPIs erfolgreich berechnet', 'DataAnalyst', {
        revenue: '782,517.00 €',
        aov: '863.71 €',
        orders: '906',
        channels: 6
      });

      // Step 5: Report Generator starts
      setCurrentStep('Bericht-Generator erstellt professionellen Bericht...');
      updateWorkflowStatus('reportGenerator', 'active');
      addLog('info', '📝 Bericht-Generator: Erstelle professionellen Fließtext-Bericht', 'ReportGenerator');
      await new Promise(resolve => setTimeout(resolve, 2500));
      
      updateWorkflowStatus('reportGenerator', 'completed');
      addLog('success', '✅ Bericht-Generator: Bericht erfolgreich erstellt', 'ReportGenerator', {
        wordCount: 377,
        sections: ['Executive Summary', 'Wichtigste Erkenntnisse', 'Handlungsempfehlungen']
      });

      // Final step
      setCurrentStep('Workflow abgeschlossen!');
      addLog('success', '🎉 Workflow erfolgreich abgeschlossen!', 'System');
      addLog('info', '📋 Vollständiger Bericht mit KPIs und Handlungsempfehlungen wurde generiert', 'System');

    } catch (error) {
      addLog('error', `❌ Fehler im Workflow: ${error.message}`, 'System');
      setCurrentStep('Fehler aufgetreten');
    } finally {
      setIsRunning(false);
    }
  }, [addLog, updateWorkflowStatus]);

  const startDemo = useCallback(async (query, demoId) => {
    if (isRunning) return;
    
    // Try to call real backend first, fallback to simulation
    try {
      abortControllerRef.current = new AbortController();
      
      addLog('info', '🔄 Verbinde mit Backend-API...', 'System');
      
      const response = await axios.post('/api/workflow/start', {
        query,
        demoId
      }, {
        timeout: 5000,
        signal: abortControllerRef.current.signal
      });
      
      if (response.data.success) {
        const workflowId = response.data.workflowId; // Backend sendet camelCase!
        setCurrentWorkflowId(workflowId);
        console.log('🔍 Backend Workflow ID gesetzt:', workflowId);
        addLog('success', '✅ Backend-API erfolgreich erreicht', 'System');
        // Handle real backend response here
        // For now, we'll still use simulation
        await simulateWorkflowProgress(query, demoId);
      }
    } catch (error) {
      if (error.name !== 'CanceledError') {
        addLog('warning', '⚠️ Backend nicht erreichbar - verwende Demo-Simulation', 'System');
        // Generate a mock workflow ID for simulation
        const mockWorkflowId = `workflow_${Date.now()}`;
        setCurrentWorkflowId(mockWorkflowId);
        console.log('🔍 Mock Workflow ID gesetzt:', mockWorkflowId);
        await simulateWorkflowProgress(query, demoId);
      }
    }
  }, [isRunning, simulateWorkflowProgress, addLog]);

  const clearLogs = useCallback(() => {
    setLogs([]);
    addLog('info', '🗑️ Logs gelöscht', 'System');
  }, [addLog]);

  const stopWorkflow = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    setIsRunning(false);
    setCurrentStep('');
    setWorkflowStatus({
      orchestrator: 'idle',
      dataAnalyst: 'idle',
      duckdbTool: 'idle', 
      reportGenerator: 'idle'
    });
    addLog('warning', '⏹️ Workflow gestoppt', 'System');
  }, [addLog]);

  return {
    workflowStatus,
    currentStep,
    logs,
    isRunning,
    currentWorkflowId,
    startDemo,
    stopWorkflow,
    clearLogs
  };
}; 