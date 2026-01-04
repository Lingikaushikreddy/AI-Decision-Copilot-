import React, { useState } from 'react';
import { Sliders, RefreshCw, Save } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import clsx from 'clsx';

const MOCK_DATA = [
    { month: 'Jan', baseline: 4000, scenario: 4000 },
    { month: 'Feb', baseline: 3000, scenario: 3200 },
    { month: 'Mar', baseline: 2000, scenario: 2500 },
    { month: 'Apr', baseline: 2780, scenario: 3500 },
    { month: 'May', baseline: 1890, scenario: 2800 },
    { month: 'Jun', baseline: 2390, scenario: 3600 },
    { month: 'Jul', baseline: 3490, scenario: 4800 },
];

export const ScenarioBuilder: React.FC = () => {
    const [marketingSpend, setMarketingSpend] = useState(-10);
    const [hiringFreeze, setHiringFreeze] = useState(true);

    return (
        <div className="w-full max-w-6xl mx-auto p-4 flex flex-col lg:flex-row gap-6 h-[80vh] animate-in fade-in zoom-in-95">

            {/* Controls Panel */}
            <div className="w-full lg:w-1/3 bg-gray-900 border border-gray-800 rounded-xl p-6 flex flex-col">
                <div className="flex items-center gap-2 mb-6 text-gray-300">
                    <Sliders className="w-5 h-5" />
                    <h2 className="font-semibold text-lg">Scenario Levers</h2>
                </div>

                <div className="space-y-8 flex-1">
                    {/* Lever 1 */}
                    <div className="space-y-3">
                        <div className="flex justify-between">
                            <label className="text-sm font-medium text-gray-300">Marketing Spend</label>
                            <span className={clsx("text-sm font-mono", marketingSpend < 0 ? "text-green-400" : "text-red-400")}>
                                {marketingSpend > 0 ? '+' : ''}{marketingSpend}%
                            </span>
                        </div>
                        <input
                            type="range"
                            min="-50"
                            max="50"
                            value={marketingSpend}
                            onChange={(e) => setMarketingSpend(parseInt(e.target.value))}
                            className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
                        />
                        <p className="text-xs text-gray-500">
                            Impact: Reduces CAC but may slow top-line growth.
                        </p>
                    </div>

                    {/* Lever 2 */}
                    <div className="space-y-3 p-4 bg-gray-800/50 rounded-lg border border-gray-700">
                        <div className="flex items-center justify-between">
                            <label className="text-sm font-medium text-gray-200">Hiring Freeze</label>
                            <button
                                onClick={() => setHiringFreeze(!hiringFreeze)}
                                className={clsx(
                                    "relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-900",
                                    hiringFreeze ? 'bg-green-500' : 'bg-gray-600'
                                )}
                            >
                                <span
                                    className={clsx(
                                        "inline-block h-4 w-4 transform rounded-full bg-white transition-transform",
                                        hiringFreeze ? 'translate-x-6' : 'translate-x-1'
                                    )}
                                />
                            </button>
                        </div>
                        <p className="text-xs text-gray-400">
                            Pauses all non-essential requisitions. Saves approx $55k/mo.
                        </p>
                    </div>
                </div>

                <div className="mt-auto flex gap-3 pt-6 border-t border-gray-800">
                    <button className="flex-1 px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-lg text-sm flex items-center justify-center gap-2">
                        <RefreshCw className="w-4 h-4" /> Reset
                    </button>
                    <button className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm flex items-center justify-center gap-2">
                        <Save className="w-4 h-4" /> Save Scenario
                    </button>
                </div>
            </div>

            {/* Chart Panel */}
            <div className="flex-1 bg-gray-900 border border-gray-800 rounded-xl p-6 relative overflow-hidden">
                {/* Glow Effect */}
                <div className="absolute top-0 right-0 w-64 h-64 bg-green-500/10 blur-[100px] rounded-full pointer-events-none" />

                <div className="flex items-center justify-between mb-8">
                    <h3 className="text-lg font-semibold text-gray-200">Projected Cash Flow</h3>
                    <div className="flex items-center gap-4 text-sm">
                        <div className="flex items-center gap-2">
                            <span className="w-3 h-0.5 bg-gray-500 mb-1"></span>
                            <span className="text-gray-400">Baseline</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <span className="w-3 h-0.5 bg-green-400 mb-1"></span>
                            <span className="text-green-400 font-medium">Scenario A</span>
                        </div>
                    </div>
                </div>

                <div className="h-[400px] w-full">
                    <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={MOCK_DATA}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                            <XAxis
                                dataKey="month"
                                stroke="#666"
                                fontSize={12}
                                tickLine={false}
                                axisLine={false}
                            />
                            <YAxis
                                stroke="#666"
                                fontSize={12}
                                tickLine={false}
                                axisLine={false}
                                tickFormatter={(val) => `$${val}`}
                            />
                            <Tooltip
                                contentStyle={{ backgroundColor: '#1f2937', borderColor: '#374151', color: '#fff' }}
                                itemStyle={{ color: '#fff' }}
                            />
                            <ReferenceLine y={2800} stroke="rgba(255,50,50,0.5)" strokeDasharray="3 3" label={{ position: 'insideTopLeft', value: 'Min Cash Threshold', fill: 'red', fontSize: 10 }} />
                            <Line
                                type="monotone"
                                dataKey="baseline"
                                stroke="#6b7280"
                                strokeWidth={2}
                                dot={false}
                                strokeDasharray="5 5"
                                activeDot={{ r: 4 }}
                            />
                            <Line
                                type="monotone"
                                dataKey="scenario"
                                stroke="#4ade80"
                                strokeWidth={3}
                                dot={false}
                                activeDot={{ r: 6, strokeWidth: 0, fill: '#fff' }}
                            />
                        </LineChart>
                    </ResponsiveContainer>
                </div>

                <div className="absolute top-6 right-6 px-4 py-2 bg-green-500/10 border border-green-500/30 rounded-full flex items-center gap-2 animate-pulse">
                    <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                    <span className="text-green-400 font-bold">+$50k Savings</span>
                </div>
            </div>
        </div>
    );
};
