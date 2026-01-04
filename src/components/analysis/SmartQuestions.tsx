import React from 'react';
import { Lightbulb, ArrowRight, TrendingUp, AlertTriangle } from 'lucide-react';
import clsx from 'clsx';

interface Question {
    id: string;
    text: string;
    type: 'opportunity' | 'risk' | 'neutral';
    impact: 'High' | 'Medium' | 'Low';
    reasoning: string;
}

const MOCK_QUESTIONS: Question[] = [
    {
        id: 'q1',
        text: 'Why is the Northeast region 15% below margin target?',
        type: 'risk',
        impact: 'High',
        reasoning: 'Variance detected in column "Region_Margin" compared to "Target_Margin".'
    },
    {
        id: 'q2',
        text: 'What if we reallocate 10% of Programmatic Spend to Organic Search?',
        type: 'opportunity',
        impact: 'Medium',
        reasoning: 'LTV/CAC ratio is 2x higher in Organic channel based on Q2 data.'
    },
    {
        id: 'q3',
        text: 'Compare Q3 marketing spend vs. Q2 trends.',
        type: 'neutral',
        impact: 'Low',
        reasoning: 'Standard quarterly variance analysis.'
    }
];

interface SmartQuestionsProps {
    onSelectQuestion: (questionId: string) => void;
}

export const SmartQuestions: React.FC<SmartQuestionsProps> = ({ onSelectQuestion }) => {
    return (
        <div className="w-full max-w-4xl mx-auto p-4 animate-in fade-in slide-in-from-bottom-8 duration-700">
            <div className="mb-8 text-center">
                <h2 className="text-2xl font-bold text-white mb-2">Analysis & Insights</h2>
                <p className="text-gray-400">Based on your upload, here are the top 3 high-impact questions you should explore.</p>
            </div>

            <div className="grid gap-4">
                {MOCK_QUESTIONS.map((q, idx) => (
                    <button
                        key={q.id}
                        onClick={() => onSelectQuestion(q.id)}
                        className="group relative bg-gray-900 border border-gray-800 hover:border-blue-500/50 rounded-xl p-6 text-left transition-all hover:bg-gray-800/50 hover:shadow-lg hover:shadow-blue-900/10"
                    >
                        <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
                            <ArrowRight className="w-5 h-5 text-blue-400" />
                        </div>

                        <div className="flex items-start gap-4">
                            <div className={clsx(
                                "w-10 h-10 rounded-lg flex items-center justify-center shrink-0",
                                q.type === 'risk' ? "bg-red-500/10 text-red-400" :
                                    q.type === 'opportunity' ? "bg-green-500/10 text-green-400" :
                                        "bg-blue-500/10 text-blue-400"
                            )}>
                                {q.type === 'risk' ? <AlertTriangle className="w-6 h-6" /> :
                                    q.type === 'opportunity' ? <TrendingUp className="w-6 h-6" /> :
                                        <Lightbulb className="w-6 h-6" />}
                            </div>

                            <div>
                                <div className="flex items-center gap-3 mb-1">
                                    <span className={clsx(
                                        "text-xs font-semibold px-2 py-0.5 rounded-full border",
                                        q.impact === 'High' ? "border-red-500/30 text-red-400 bg-red-500/5" :
                                            q.impact === 'Medium' ? "border-yellow-500/30 text-yellow-400 bg-yellow-500/5" :
                                                "border-gray-600 text-gray-400"
                                    )}>
                                        {q.impact} Impact
                                    </span>
                                    <span className="text-xs text-gray-500">Ranked #{idx + 1}</span>
                                </div>

                                <h3 className="text-lg font-medium text-white mb-2 group-hover:text-blue-300 transition-colors">
                                    {q.text}
                                </h3>

                                <p className="text-sm text-gray-500 font-mono border-l-2 border-gray-700 pl-3">
                                    AI Logic: {q.reasoning}
                                </p>
                            </div>
                        </div>
                    </button>
                ))}
            </div>
        </div>
    );
};
