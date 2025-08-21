import React, { useState } from 'react';
import { Play, BarChart3, TrendingUp, DollarSign, Loader2 } from 'lucide-react';

const DemoCases = ({ onStartDemo, isRunning }) => {
  const [selectedDemo, setSelectedDemo] = useState(null);

  const demoCases = [
    {
      id: 'revenue-aov',
      title: 'Umsatz & AOV Analyse',
      description: 'Analysiert den Gesamtumsatz und durchschnittlichen Bestellwert für das E-Commerce Business',
      icon: DollarSign,
      color: 'bg-green-100 text-green-600',
      query: 'Analysiere den Gesamtumsatz und AOV für unser E-Commerce Business',
      expectedKPIs: ['Gesamtumsatz', 'Average Order Value', 'Anzahl Bestellungen'],
      estimatedTime: '2-3 Minuten'
    },
    {
      id: 'channel-performance',
      title: 'Akquisitionskanal Performance',
      description: 'Vergleicht die Performance aller Marketing-Kanäle in Bezug auf Umsatz und Bestellungen',
      icon: TrendingUp,
      color: 'bg-blue-100 text-blue-600',
      query: 'Wie performt jeder Akquisitionskanal in Bezug auf Umsatz und Anzahl Bestellungen?',
      expectedKPIs: ['Umsatz pro Kanal', 'Bestellungen pro Kanal', 'Conversion Rates'],
      estimatedTime: '2-3 Minuten'
    },
    {
      id: 'gross-margin',
      title: 'Gross Margin Berechnung',
      description: 'Berechnet die Bruttomarge für das gesamte Produktportfolio und identifiziert profitabelste Bereiche',
      icon: BarChart3,
      color: 'bg-purple-100 text-purple-600',
      query: 'Berechne die Gross Margin für unser Produktportfolio',
      expectedKPIs: ['Gross Margin %', 'COGS', 'Profitabilität nach Kategorie'],
      estimatedTime: '2-3 Minuten'
    }
  ];

  const handleStartDemo = (demoCase) => {
    setSelectedDemo(demoCase.id);
    onStartDemo(demoCase.query, demoCase.id);
  };

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          🎬 Demo Cases
        </h2>
        <p className="text-gray-600">
          Starte eine der vorkonfigurierten Analysen und verfolge den Workflow live
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-1 lg:grid-cols-1">
        {demoCases.map((demoCase) => {
          const Icon = demoCase.icon;
          const isSelected = selectedDemo === demoCase.id;
          const isCurrentlyRunning = isRunning && isSelected;
          
          return (
            <div
              key={demoCase.id}
              className={`demo-card p-6 ${isSelected ? 'ring-2 ring-primary-500' : ''}`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-4 flex-1">
                  <div className={`p-3 rounded-lg ${demoCase.color}`}>
                    <Icon className="w-6 h-6" />
                  </div>
                  
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      {demoCase.title}
                    </h3>
                    <p className="text-gray-600 mb-4">
                      {demoCase.description}
                    </p>
                    
                    <div className="space-y-3">
                      <div>
                        <h4 className="text-sm font-medium text-gray-700 mb-1">
                          Erwartete KPIs:
                        </h4>
                        <div className="flex flex-wrap gap-2">
                          {demoCase.expectedKPIs.map((kpi, index) => (
                            <span
                              key={index}
                              className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full"
                            >
                              {kpi}
                            </span>
                          ))}
                        </div>
                      </div>
                      
                      <div className="flex items-center justify-between text-sm text-gray-500">
                        <span>⏱️ Geschätzte Dauer: {demoCase.estimatedTime}</span>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="ml-4">
                  <button
                    onClick={() => handleStartDemo(demoCase)}
                    disabled={isRunning}
                    className={`
                      flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all
                      ${isCurrentlyRunning
                        ? 'bg-blue-500 text-white cursor-not-allowed'
                        : isRunning
                        ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                        : 'bg-primary-500 hover:bg-primary-600 text-white hover:shadow-lg'
                      }
                    `}
                  >
                    {isCurrentlyRunning ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        Läuft...
                      </>
                    ) : (
                      <>
                        <Play className="w-4 h-4" />
                        Demo starten
                      </>
                    )}
                  </button>
                </div>
              </div>
              
              {isSelected && (
                <div className="mt-4 p-3 bg-blue-50 rounded-lg border-l-4 border-blue-400">
                  <p className="text-sm text-blue-800">
                    <strong>Query:</strong> "{demoCase.query}"
                  </p>
                </div>
              )}
            </div>
          );
        })}
      </div>
      
      {isRunning && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex items-center gap-2">
            <Loader2 className="w-5 h-5 text-yellow-600 animate-spin" />
            <span className="font-medium text-yellow-800">
              Workflow läuft...
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

export default DemoCases; 