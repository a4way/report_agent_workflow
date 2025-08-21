import React, { useEffect, useRef, useState, useCallback } from 'react';
import { 
  Info, 
  CheckCircle, 
  AlertTriangle, 
  XCircle, 
  Terminal,
  Download,
  Trash2,
  ArrowDown,
  Pause
} from 'lucide-react';

const LogPanel = ({ logs, onClearLogs }) => {
  const logEndRef = useRef(null);
  const logContainerRef = useRef(null);
  const [autoScroll, setAutoScroll] = useState(false);

  const scrollToBottom = useCallback(() => {
    if (autoScroll && logEndRef.current) {
      logEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [autoScroll]);

  const handleManualScroll = () => {
    if (logContainerRef.current) {
      const { scrollTop, scrollHeight, clientHeight } = logContainerRef.current;
      const isAtBottom = Math.abs(scrollHeight - scrollTop - clientHeight) < 5; // 5px Toleranz
      
      // Auto-scroll nur aktivieren, wenn User ganz unten ist
      if (isAtBottom && !autoScroll) {
        setAutoScroll(true);
      } else if (!isAtBottom && autoScroll) {
        setAutoScroll(false);
      }
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [logs, scrollToBottom]);

  const getLogIcon = (level) => {
    switch (level) {
      case 'success':
        return <CheckCircle className="w-4 h-4" />;
      case 'warning':
        return <AlertTriangle className="w-4 h-4" />;
      case 'error':
        return <XCircle className="w-4 h-4" />;
      default:
        return <Info className="w-4 h-4" />;
    }
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('de-DE', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      fractionalSecondDigits: 3
    });
  };

  const exportLogs = () => {
    const logText = logs.map(log => 
      `[${formatTimestamp(log.timestamp)}] ${log.level.toUpperCase()}: ${log.message}`
    ).join('\n');
    
    const blob = new Blob([logText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `langgraph-workflow-logs-${new Date().toISOString().slice(0, 19)}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="bg-white rounded-lg shadow-lg border border-gray-200 flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        <div className="flex items-center gap-2">
          <Terminal className="w-5 h-5 text-gray-600" />
          <h3 className="font-semibold text-gray-900">Workflow Logs</h3>
          <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
            {logs.length} Einträge
          </span>
        </div>
        
        <div className="flex items-center gap-2">
          <button
            onClick={() => setAutoScroll(!autoScroll)}
            className={`p-2 rounded-md transition-colors ${
              autoScroll 
                ? 'text-blue-600 bg-blue-50 hover:bg-blue-100' 
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
            }`}
            title={autoScroll ? "Auto-Scroll deaktivieren" : "Auto-Scroll aktivieren"}
          >
            {autoScroll ? <ArrowDown className="w-4 h-4" /> : <Pause className="w-4 h-4" />}
          </button>
          <button
            onClick={exportLogs}
            disabled={logs.length === 0}
            className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            title="Logs exportieren"
          >
            <Download className="w-4 h-4" />
          </button>
          <button
            onClick={onClearLogs}
            disabled={logs.length === 0}
            className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            title="Logs löschen"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Log Content */}
      <div 
        ref={logContainerRef}
        onScroll={handleManualScroll}
        className="flex-1 overflow-y-auto p-4 space-y-2 bg-gray-50"
      >
        {logs.length === 0 ? (
          <div className="text-center py-8">
            <Terminal className="w-12 h-12 text-gray-300 mx-auto mb-3" />
            <p className="text-gray-500">Keine Logs vorhanden</p>
            <p className="text-sm text-gray-400 mt-1">
              Starte einen Demo-Case um Logs zu sehen
            </p>
          </div>
        ) : (
          <>
            {logs.map((log, index) => (
              <div
                key={index}
                className={`log-entry ${log.level}`}
              >
                <div className="flex items-start gap-2">
                  <div className="flex-shrink-0 mt-0.5">
                    {getLogIcon(log.level)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xs font-medium opacity-75">
                        {formatTimestamp(log.timestamp)}
                      </span>
                      {log.agent && (
                        <span className="text-xs px-2 py-0.5 bg-white bg-opacity-50 rounded">
                          {log.agent}
                        </span>
                      )}
                    </div>
                    <p className="text-sm leading-relaxed break-words">
                      {log.message}
                    </p>
                    {log.details && (
                      <details className="mt-2">
                        <summary className="text-xs cursor-pointer hover:underline opacity-75">
                          Details anzeigen
                        </summary>
                        <pre className="text-xs mt-1 p-2 bg-white bg-opacity-50 rounded overflow-x-auto">
                          {typeof log.details === 'string' ? log.details : JSON.stringify(log.details, null, 2)}
                        </pre>
                      </details>
                    )}
                  </div>
                </div>
              </div>
            ))}
            <div ref={logEndRef} />
          </>
        )}
      </div>

      {/* Footer Stats */}
      {logs.length > 0 && (
        <div className="p-3 border-t border-gray-200 bg-gray-50">
          <div className="flex justify-between text-xs text-gray-500">
            <div className="flex gap-4">
              <span>ℹ️ Info: {logs.filter(l => l.level === 'info').length}</span>
              <span>✅ Success: {logs.filter(l => l.level === 'success').length}</span>
              <span>⚠️ Warning: {logs.filter(l => l.level === 'warning').length}</span>
              <span>❌ Error: {logs.filter(l => l.level === 'error').length}</span>
            </div>
            <span>Letzte Aktualisierung: {logs.length > 0 ? formatTimestamp(logs[logs.length - 1].timestamp) : 'Nie'}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default LogPanel; 