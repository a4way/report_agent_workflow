import React, { useState } from 'react';
import { Play, ChevronDown, BarChart3, TrendingUp, DollarSign, Loader2, Clock } from 'lucide-react';

const DemoSelector = ({ onStartDemo, isRunning }) => {
  const [selectedDemo, setSelectedDemo] = useState('');
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const demoCases = [
    {
      id: 'revenue-aov',
      title: 'Umsatz & AOV Analyse',
      description: 'Analysiert den Gesamtumsatz und durchschnittlichen Bestellwert',
      icon: DollarSign,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
      query: 'Analysiere den Gesamtumsatz und AOV für unser E-Commerce Business',
      expectedKPIs: ['Gesamtumsatz', 'Average Order Value', 'Anzahl Bestellungen'],
      estimatedTime: '2-3 Minuten'
    },
    {
      id: 'channel-performance',
      title: 'Akquisitionskanal Performance',
      description: 'Vergleicht die Performance aller Marketing-Kanäle',
      icon: TrendingUp,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      query: 'Wie performt jeder Akquisitionskanal in Bezug auf Umsatz und Anzahl Bestellungen?',
      expectedKPIs: ['Umsatz pro Kanal', 'Bestellungen pro Kanal', 'Conversion Rates'],
      estimatedTime: '2-3 Minuten'
    },
    {
      id: 'gross-margin',
      title: 'Gross Margin Berechnung',
      description: 'Berechnet die Bruttomarge für das gesamte Produktportfolio',
      icon: BarChart3,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
      query: 'Berechne die Gross Margin für unser Produktportfolio',
      expectedKPIs: ['Gross Margin %', 'COGS', 'Profitabilität nach Kategorie'],
      estimatedTime: '2-3 Minuten'
    }
  ];

  const selectedDemoData = demoCases.find(demo => demo.id === selectedDemo);

  const handleSelectDemo = (demoId) => {
    setSelectedDemo(demoId);
    setIsDropdownOpen(false);
  };

  const handleStartDemo = () => {
    if (selectedDemoData && !isRunning) {
      onStartDemo(selectedDemoData.query, selectedDemoData.id);
    }
  };

  return (
    <div className="space-y-4">
      <div className="text-center">
        <h2 className="text-xl font-bold text-gray-900 mb-2 flex items-center justify-center gap-2">
          🎬 Demo Cases
        </h2>
        <p className="text-gray-600 text-sm">
          Wähle eine Analyse aus und starte den Workflow
        </p>
      </div>

      {/* Demo Selector Dropdown */}
      <div className="relative">
        <button
          onClick={() => setIsDropdownOpen(!isDropdownOpen)}
          disabled={isRunning}
          className="w-full flex items-center justify-between px-4 py-3 bg-white border border-gray-300 rounded-lg shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <div className="flex items-center gap-3">
            {selectedDemoData ? (
              <>
                <div className={`p-2 rounded-lg ${selectedDemoData.bgColor}`}>
                  <selectedDemoData.icon className={`w-5 h-5 ${selectedDemoData.color}`} />
                </div>
                <div className="text-left">
                  <div className="font-medium text-gray-900">{selectedDemoData.title}</div>
                  <div className="text-sm text-gray-500">{selectedDemoData.description}</div>
                </div>
              </>
            ) : (
              <>
                <div className="p-2 rounded-lg bg-gray-100">
                  <BarChart3 className="w-5 h-5 text-gray-400" />
                </div>
                <div className="text-left">
                  <div className="font-medium text-gray-500">Demo Case auswählen...</div>
                  <div className="text-sm text-gray-400">Wähle eine der 3 verfügbaren Analysen</div>
                </div>
              </>
            )}
          </div>
          <ChevronDown className={`w-5 h-5 text-gray-400 transition-transform ${isDropdownOpen ? 'rotate-180' : ''}`} />
        </button>

        {/* Dropdown Menu */}
        {isDropdownOpen && (
          <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg z-50 max-h-96 overflow-y-auto">
            {demoCases.map((demoCase) => {
              const Icon = demoCase.icon;
              return (
                <button
                  key={demoCase.id}
                  onClick={() => handleSelectDemo(demoCase.id)}
                  className="w-full text-left px-4 py-3 hover:bg-gray-50 focus:bg-gray-50 focus:outline-none first:rounded-t-lg last:rounded-b-lg border-b border-gray-100 last:border-b-0"
                >
                  <div className="flex items-start gap-3">
                    <div className={`p-2 rounded-lg ${demoCase.bgColor} flex-shrink-0`}>
                      <Icon className={`w-5 h-5 ${demoCase.color}`} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="font-medium text-gray-900">{demoCase.title}</div>
                      <div className="text-sm text-gray-600 mt-1">{demoCase.description}</div>
                      <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                        <span className="flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          {demoCase.estimatedTime}
                        </span>
                        <span>{demoCase.expectedKPIs.length} KPIs</span>
                      </div>
                    </div>
                  </div>
                </button>
              );
            })}
          </div>
        )}
      </div>

      {/* Selected Demo Details */}
      {selectedDemoData && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-medium text-blue-900">Ausgewählte Analyse</h3>
            <span className="text-xs text-blue-600 bg-blue-100 px-2 py-1 rounded-full">
              {selectedDemoData.estimatedTime}
            </span>
          </div>
          
          <div className="space-y-2 mb-4">
            <div>
              <span className="text-sm font-medium text-blue-800">Query: </span>
              <span className="text-sm text-blue-700">"{selectedDemoData.query}"</span>
            </div>
            <div>
              <span className="text-sm font-medium text-blue-800">Erwartete KPIs: </span>
              <div className="flex flex-wrap gap-1 mt-1">
                {selectedDemoData.expectedKPIs.map((kpi, index) => (
                  <span
                    key={index}
                    className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full"
                  >
                    {kpi}
                  </span>
                ))}
              </div>
            </div>
          </div>

          <button
            onClick={handleStartDemo}
            disabled={isRunning}
            className={`
              w-full flex items-center justify-center gap-2 px-4 py-3 rounded-lg font-medium transition-all
              ${isRunning
                ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                : 'bg-primary-500 hover:bg-primary-600 text-white hover:shadow-lg'
              }
            `}
          >
            {isRunning ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Workflow läuft...
              </>
            ) : (
              <>
                <Play className="w-5 h-5" />
                Demo starten
              </>
            )}
          </button>
        </div>
      )}

      {isRunning && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex items-center gap-2">
            <Loader2 className="w-5 h-5 text-yellow-600 animate-spin" />
            <span className="font-medium text-yellow-800">
              Workflow wird ausgeführt...
            </span>
          </div>
          <p className="text-sm text-yellow-700 mt-1">
            Verfolge den Fortschritt im Workflow-Graph und im Log-Bereich.
          </p>
        </div>
      )}
    </div>
  );
};

export default DemoSelector; 