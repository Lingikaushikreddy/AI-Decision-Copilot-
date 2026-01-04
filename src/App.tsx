import { useState } from 'react';

import { FileUploader } from './components/ingest/FileUploader';
import { SmartQuestions } from './components/analysis/SmartQuestions';
import { ScenarioBuilder } from './components/scenarios/ScenarioBuilder';
import { DecisionMemo } from './components/output/DecisionMemo';
import { BrainCircuit } from 'lucide-react';
import clsx from 'clsx';

const STEPS = [
  { label: 'Upload', id: 'upload' },
  { label: 'Analysis', id: 'analysis' },
  { label: 'Scenarios', id: 'scenarios' },
  { label: 'Decision', id: 'output' },
] as const;

function App() {
  const [currentStep, setCurrentStep] = useState<'upload' | 'analysis' | 'scenarios' | 'output'>('upload');
  const [activeFile, setActiveFile] = useState<File | null>(null);

  const handleUpload = (file: File) => {
    setActiveFile(file);
    // Simulate processing delay
    setTimeout(() => {
      setCurrentStep('analysis');
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 font-sans selection:bg-blue-500/30">
      {/* Header */}
      <header className="border-b border-gray-800 bg-gray-900/50 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <BrainCircuit className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-xl tracking-tight">AI Decision Copilot</span>
          </div>

          <nav className="flex items-center gap-1 bg-gray-800/50 rounded-full p-1 border border-gray-700">
            {STEPS.map((step, idx) => {
              const isActive = step.id === currentStep;

              return (
                <button
                  key={step.id}
                  onClick={() => {
                    if (activeFile) {
                      setCurrentStep(step.id);
                    }
                  }}
                  className={clsx(
                    "px-4 py-1.5 rounded-full text-sm font-medium transition-all duration-200",
                    isActive
                      ? "bg-gray-700 text-white shadow-sm"
                      : "text-gray-400 hover:text-gray-200"
                  )}
                  disabled={!activeFile && idx > 0}
                >
                  {step.label}
                </button>
              );
            })}
          </nav>

          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-gray-700 border border-gray-600" />
            <span className="text-sm font-medium text-gray-300">Finance Mgr</span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {currentStep === 'upload' && (
          <div className="flex flex-col items-center justify-center min-h-[60vh] animate-in fade-in zoom-in-95 duration-500">
            <div className="text-center mb-10 max-w-xl">
              <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                Power Your Decisions with Data
              </h1>
              <p className="text-gray-400 text-lg">
                Upload your datasets to unlock predictive insights, scenario modeling, and exec-ready decision memos.
              </p>
            </div>
            <FileUploader onFileUpload={handleUpload} />
          </div>
        )}

        {currentStep === 'analysis' && (
          <div className="py-10">
            <SmartQuestions onSelectQuestion={() => setCurrentStep('scenarios')} />
            <div className="text-center mt-12">
              <button
                onClick={() => setCurrentStep('scenarios')}
                className="text-sm text-gray-500 hover:text-white underline"
              >
                Skip Analysis
              </button>
            </div>
          </div>
        )}

        {currentStep === 'scenarios' && (
          <div className="py-4">
            <ScenarioBuilder />
            <div className="flex justify-center mt-8">
              <button
                onClick={() => setCurrentStep('output')}
                className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-xl font-semibold shadow-lg shadow-blue-900/20 transition-all hover:scale-105"
              >
                Generate Final Memo
              </button>
            </div>
          </div>
        )}

        {currentStep === 'output' && (
          <div className="py-4">
            <div className="flex justify-start mb-6">
              <button onClick={() => setCurrentStep('scenarios')} className="text-gray-400 hover:text-white flex items-center gap-2">
                ← Back to Scenarios
              </button>
            </div>
            <DecisionMemo />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
