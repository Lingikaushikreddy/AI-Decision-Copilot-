import React from 'react';
import { Share2, Download, ShieldCheck, AlertOctagon } from 'lucide-react';

export const DecisionMemo: React.FC = () => {
    return (
        <div className="w-full max-w-4xl mx-auto p-8 bg-white text-gray-900 rounded-xl shadow-2xl animate-in zoom-in-95 duration-500">

            {/* Header */}
            <div className="flex justify-between items-start mb-8 border-b border-gray-200 pb-6">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">Recommendation: Implement Hiring Freeze</h1>
                    <p className="text-gray-500 text-sm">Generated on Oct 24, 2024 • ID: #MEMO-4921</p>
                </div>
                <div className="flex items-center gap-2 px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-semibold border border-green-200">
                    <ShieldCheck className="w-4 h-4" />
                    Confidence: High (85%)
                </div>
            </div>

            {/* BLUF */}
            <section className="mb-8">
                <h2 className="text-xs uppercase tracking-wider text-gray-500 font-bold mb-3">Bottom Line Up Front (BLUF)</h2>
                <p className="text-lg leading-relaxed font-serif">
                    Based on Q3 revenue variance analysis, we recommend an immediate <strong>hiring freeze for all non-engineering roles</strong>.
                    This action protects Q4 EBITDA margins (projected +$600k savings) with minimal risk to product roadmap delivery.
                </p>
            </section>

            {/* Evidence */}
            <section className="mb-8 p-6 bg-gray-50 rounded-lg border border-gray-100">
                <h2 className="text-xs uppercase tracking-wider text-gray-500 font-bold mb-4">Supporting Evidence</h2>
                <ul className="space-y-4">
                    <li className="flex gap-3 items-start">
                        <span className="w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-xs font-bold shrink-0">1</span>
                        <div>
                            <h4 className="font-semibold text-sm">Revenue Miss</h4>
                            <p className="text-sm text-gray-600">Northeast region is trending 15% below target, creating a $1.2M gap.</p>
                        </div>
                    </li>
                    <li className="flex gap-3 items-start">
                        <span className="w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-xs font-bold shrink-0">2</span>
                        <div>
                            <h4 className="font-semibold text-sm">Headcount Costs</h4>
                            <p className="text-sm text-gray-600">Current open reqs account for 40% of projected Q4 OpEx growth.</p>
                        </div>
                    </li>
                </ul>
            </section>

            {/* Trade-offs & Risks */}
            <section className="mb-8">
                <h2 className="text-xs uppercase tracking-wider text-gray-500 font-bold mb-3">Trade-offs & Risks</h2>
                <div className="rounded-l-4 border-l-4 border-yellow-500 bg-yellow-50 p-4">
                    <div className="flex gap-3">
                        <AlertOctagon className="w-5 h-5 text-yellow-600" />
                        <div>
                            <h4 className="font-bold text-yellow-800 text-sm">Wait Times</h4>
                            <p className="text-sm text-yellow-700 mt-1">
                                Customer support response times may increase by 12% due to frozen support reqs.
                                <em>(Source: Operations Capacity Model)</em>
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Footer Actions */}
            <div className="flex gap-4 mt-12 pt-6 border-t border-gray-100">
                <button className="flex-1 bg-gray-900 text-white px-4 py-3 rounded-lg font-medium hover:bg-gray-800 transition-colors flex items-center justify-center gap-2">
                    <Download className="w-4 h-4" /> Export to PDF
                </button>
                <button className="px-6 py-3 border border-gray-300 rounded-lg font-medium hover:bg-gray-50 transition-colors flex items-center justify-center gap-2 text-gray-700">
                    <Share2 className="w-4 h-4" /> Share
                </button>
            </div>

        </div>
    );
};
