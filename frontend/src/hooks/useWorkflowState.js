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
  const [finalResult, setFinalResult] = useState('');
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

  const pollBackendWorkflowProgress = useCallback(async (workflowId) => {
    try {
      let isCompleted = false;
      let pollCount = 0;
      const maxPolls = 60; // 60 seconds max
      
      while (!isCompleted && pollCount < maxPolls && !abortControllerRef.current?.signal.aborted) {
        // Poll backend for status and logs
        const [statusResponse, logsResponse] = await Promise.all([
          axios.get(`/api/workflow/${workflowId}/status`, {
            signal: abortControllerRef.current?.signal
          }),
          axios.get(`/api/workflow/${workflowId}/logs`, {
            signal: abortControllerRef.current?.signal
          })
        ]);

        const workflowData = statusResponse.data;
        const logsData = logsResponse.data;
        
        // Update UI state based on real backend status
        if (workflowData.workflow_status) {
          setWorkflowStatus(workflowData.workflow_status);
        }
        if (workflowData.current_step) {
          setCurrentStep(workflowData.current_step);
        }

        // Update logs with real backend logs
        if (logsData.logs && logsData.logs.length > 0) {
          setLogs(logsData.logs);
        }

        // Update final result if available
        if (workflowData.final_result) {
          setFinalResult(workflowData.final_result);
        }

        // Check if workflow is completed
        if (workflowData.status === 'completed') {
          isCompleted = true;
          setIsRunning(false);
          addLog('success', '🎉 LangGraph-Analyse erfolgreich abgeschlossen!', 'System');
        } else if (workflowData.status === 'failed') {
          isCompleted = true;
          setIsRunning(false);
          addLog('error', '❌ Workflow fehlgeschlagen', 'System');
        }

        // Wait before next poll (if not completed)
        if (!isCompleted) {
          await new Promise(resolve => setTimeout(resolve, 1000)); // Poll every second
          pollCount++;
        }
      }
      
      if (pollCount >= maxPolls) {
        addLog('warning', '⚠️ Workflow-Polling Timeout erreicht', 'System');
        setIsRunning(false);
      }
      
    } catch (error) {
      if (error.name !== 'CanceledError') {
        console.error('Fehler beim Backend-Polling:', error);
        addLog('error', `❌ Fehler beim Abrufen der Workflow-Daten: ${error.message}`, 'System');
        setIsRunning(false);
      }
    }
  }, []);

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
        signal: abortControllerRef.current?.signal
      });

      if (response.data.success) {
        const workflowId = response.data.workflowId; // Backend sendet camelCase!
        setCurrentWorkflowId(workflowId);
        console.log('🔍 Backend Workflow ID gesetzt:', workflowId);
        addLog('success', '✅ Backend-API erfolgreich erreicht', 'System');
        // Handle real backend response - poll for real logs
        await pollBackendWorkflowProgress(workflowId);
      }
    } catch (error) {
      if (error.name !== 'CanceledError') {
        addLog('error', '❌ Backend nicht erreichbar - kann keine Analyse durchführen', 'System');
        addLog('error', '🔧 Bitte stelle sicher, dass das Backend läuft: python3 web_api.py', 'System');
        setIsRunning(false);
      }
    }
  }, [isRunning, addLog]);

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
    finalResult,
    startDemo,
    stopWorkflow,
    clearLogs
  };
}; 