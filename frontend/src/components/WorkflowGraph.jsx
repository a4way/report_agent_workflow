import React, { useMemo } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  Handle,
  Position,
} from 'react-flow-renderer';
import { 
  Brain, 
  Database, 
  BarChart3, 
  FileText, 
  CheckCircle2, 
  Clock, 
  Zap
} from 'lucide-react';

const nodeTypes = {
  orchestrator: ({ data }) => (
    <div className={`workflow-node ${data.status || ''}`}>
      <Handle type="target" position={Position.Top} />
      <div className="flex items-center gap-3">
        <div className="p-2 bg-purple-100 rounded-lg">
          <Zap className="w-6 h-6 text-purple-600" />
        </div>
        <div>
          <h3 className="font-semibold text-gray-800">{data.label}</h3>
          <p className="text-sm text-gray-600">{data.description}</p>
          {data.status === 'active' && (
            <div className="flex items-center gap-1 mt-1">
              <Clock className="w-4 h-4 text-blue-500 animate-spin-slow" />
              <span className="text-xs text-blue-600">Verarbeitung...</span>
            </div>
          )}
          {data.status === 'completed' && (
            <div className="flex items-center gap-1 mt-1">
              <CheckCircle2 className="w-4 h-4 text-green-500" />
              <span className="text-xs text-green-600">Abgeschlossen</span>
            </div>
          )}
        </div>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  ),
  
  dataAnalyst: ({ data }) => (
    <div className={`workflow-node ${data.status || ''}`}>
      <Handle type="target" position={Position.Top} />
      <div className="flex items-center gap-3">
        <div className="p-2 bg-blue-100 rounded-lg">
          <BarChart3 className="w-6 h-6 text-blue-600" />
        </div>
        <div>
          <h3 className="font-semibold text-gray-800">{data.label}</h3>
          <p className="text-sm text-gray-600">{data.description}</p>
          {data.status === 'active' && (
            <div className="flex items-center gap-1 mt-1">
              <Brain className="w-4 h-4 text-blue-500 animate-pulse" />
              <span className="text-xs text-blue-600">Analysiert Daten...</span>
            </div>
          )}
          {data.status === 'completed' && (
            <div className="flex items-center gap-1 mt-1">
              <CheckCircle2 className="w-4 h-4 text-green-500" />
              <span className="text-xs text-green-600">KPIs berechnet</span>
            </div>
          )}
        </div>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  ),
  
  reportGenerator: ({ data }) => (
    <div className={`workflow-node ${data.status || ''}`}>
      <Handle type="target" position={Position.Top} />
      <div className="flex items-center gap-3">
        <div className="p-2 bg-green-100 rounded-lg">
          <FileText className="w-6 h-6 text-green-600" />
        </div>
        <div>
          <h3 className="font-semibold text-gray-800">{data.label}</h3>
          <p className="text-sm text-gray-600">{data.description}</p>
          {data.status === 'active' && (
            <div className="flex items-center gap-1 mt-1">
              <FileText className="w-4 h-4 text-green-500 animate-pulse" />
              <span className="text-xs text-green-600">Erstellt Bericht...</span>
            </div>
          )}
          {data.status === 'completed' && (
            <div className="flex items-center gap-1 mt-1">
              <CheckCircle2 className="w-4 h-4 text-green-500" />
              <span className="text-xs text-green-600">Bericht fertig</span>
            </div>
          )}
        </div>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  ),
  
  duckdbTool: ({ data }) => (
    <div className={`workflow-node ${data.status || ''}`}>
      <Handle type="target" position={Position.Top} />
      <div className="flex items-center gap-3">
        <div className="p-2 bg-orange-100 rounded-lg">
          <Database className="w-6 h-6 text-orange-600" />
        </div>
        <div>
          <h3 className="font-semibold text-gray-800">{data.label}</h3>
          <p className="text-sm text-gray-600">{data.description}</p>
          {data.status === 'active' && (
            <div className="flex items-center gap-1 mt-1">
              <Database className="w-4 h-4 text-orange-500 animate-bounce-slow" />
              <span className="text-xs text-orange-600">SQL Query läuft...</span>
            </div>
          )}
          {data.status === 'completed' && (
            <div className="flex items-center gap-1 mt-1">
              <CheckCircle2 className="w-4 h-4 text-green-500" />
              <span className="text-xs text-green-600">Daten abgerufen</span>
            </div>
          )}
        </div>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  ),
};

const WorkflowGraph = ({ workflowStatus, currentStep }) => {
  const initialNodes = useMemo(() => [
    {
      id: 'orchestrator',
      type: 'orchestrator',
      position: { x: 300, y: 50 },
      data: {
        label: '🎯 Orchestrator',
        description: 'Koordiniert den Workflow',
        status: workflowStatus.orchestrator || 'idle'
      },
    },
    {
      id: 'dataAnalyst',
      type: 'dataAnalyst',
      position: { x: 100, y: 200 },
      data: {
        label: '📊 Datenanalyse-Agent',
        description: 'Berechnet KPIs und analysiert',
        status: workflowStatus.dataAnalyst || 'idle'
      },
    },
    {
      id: 'duckdbTool',
      type: 'duckdbTool',
      position: { x: 100, y: 350 },
      data: {
        label: '🔧 DuckDB Tool',
        description: 'SQL-Queries auf CSV-Daten',
        status: workflowStatus.duckdbTool || 'idle'
      },
    },
    {
      id: 'reportGenerator',
      type: 'reportGenerator',
      position: { x: 500, y: 200 },
      data: {
        label: '📝 Bericht-Generator',
        description: 'Erstellt professionelle Berichte',
        status: workflowStatus.reportGenerator || 'idle'
      },
    },
  ], [workflowStatus]);

  const initialEdges = useMemo(() => [
    // Einfache Test-Edges erst mal
    {
      id: 'orchestrator-dataAnalyst',
      source: 'orchestrator',
      target: 'dataAnalyst',
      type: 'smoothstep',
      style: { stroke: '#3b82f6', strokeWidth: 2 }
    },
    {
      id: 'orchestrator-reportGenerator',
      source: 'orchestrator',
      target: 'reportGenerator', 
      type: 'smoothstep',
      style: { stroke: '#8b5cf6', strokeWidth: 2 }
    },
    {
      id: 'dataAnalyst-duckdbTool',
      source: 'dataAnalyst',
      target: 'duckdbTool',
      type: 'smoothstep',
      style: { stroke: '#f59e0b', strokeWidth: 2 }
    },
    {
      id: 'duckdbTool-dataAnalyst-return',
      source: 'duckdbTool',
      target: 'dataAnalyst',
      type: 'smoothstep',
      style: { stroke: '#10b981', strokeWidth: 2 }
    }
  ], [workflowStatus]);

  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  // Update nodes when workflowStatus changes
  React.useEffect(() => {
    setNodes(initialNodes);
  }, [initialNodes, setNodes]);

  React.useEffect(() => {
    setEdges(initialEdges);
  }, [initialEdges, setEdges]);

  return (
    <div className="h-full w-full bg-gradient-to-br from-blue-50 to-purple-50">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        nodeTypes={nodeTypes}
        fitView
        attributionPosition="bottom-left"
        connectionLineType="smoothstep"
        defaultEdgeOptions={{
          type: 'smoothstep',
          animated: false,
          style: { strokeWidth: 2 }
        }}
      >
        <Background color="#e5e7eb" gap={20} />
        <Controls />
        <MiniMap
          nodeColor={(node) => {
            switch (node.data?.status) {
              case 'active': return '#3b82f6';
              case 'completed': return '#10b981';
              case 'error': return '#ef4444';
              default: return '#6b7280';
            }
          }}
          nodeStrokeWidth={3}
          className="bg-white border border-gray-200 rounded-lg"
        />
      </ReactFlow>
      
      {/* Current Step Indicator */}
      {currentStep && (
        <div className="absolute top-4 left-4 bg-white rounded-lg shadow-lg p-4 border border-gray-200">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
            <span className="font-semibold text-gray-800">Aktueller Schritt:</span>
          </div>
          <p className="text-sm text-gray-600 mt-1">{currentStep}</p>
        </div>
      )}
    </div>
  );
};

export default WorkflowGraph; 