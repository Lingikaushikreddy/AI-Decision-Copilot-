import React, { useCallback, useState } from 'react';
import { Upload, CheckCircle, AlertCircle } from 'lucide-react';

import clsx from 'clsx';

interface FileUploaderProps {
    onFileUpload: (file: File) => void;
}

export const FileUploader: React.FC<FileUploaderProps> = ({ onFileUpload }) => {
    const [isDragging, setIsDragging] = useState(false);
    const [uploadedFile, setUploadedFile] = useState<File | null>(null);

    const handleDragOver = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    }, []);

    const handleDragLeave = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
    }, []);

    const handleDrop = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            setUploadedFile(file);
            onFileUpload(file);
        }
    }, [onFileUpload]);

    const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            const file = e.target.files[0];
            setUploadedFile(file);
            onFileUpload(file);
        }
    }, [onFileUpload]);

    return (
        <div className="w-full max-w-2xl mx-auto p-4">
            <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={clsx(
                    "relative border-2 border-dashed rounded-xl p-8 transition-colors duration-200 ease-in-out flex flex-col items-center justify-center gap-4 cursor-pointer",
                    isDragging
                        ? "border-blue-500 bg-blue-500/10"
                        : "border-gray-600 hover:border-gray-500 bg-gray-800/50"
                )}
            >
                <input
                    type="file"
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    onChange={handleFileInput}
                    accept=".csv,.xlsx,.json,.pdf"
                />

                {uploadedFile ? (
                    <>
                        <div className="w-16 h-16 rounded-full bg-green-500/20 flex items-center justify-center">
                            <CheckCircle className="w-8 h-8 text-green-500" />
                        </div>
                        <div className="text-center">
                            <p className="text-lg font-medium text-white">{uploadedFile.name}</p>
                            <p className="text-sm text-gray-400">{(uploadedFile.size / 1024).toFixed(2)} KB</p>
                        </div>
                        <button
                            className="mt-2 text-sm text-gray-400 hover:text-white underline z-10"
                            onClick={(e) => {
                                e.stopPropagation();
                                setUploadedFile(null);
                            }}
                        >
                            Remove file
                        </button>
                    </>
                ) : (
                    <>
                        <div className="w-16 h-16 rounded-full bg-gray-700 flex items-center justify-center">
                            <Upload className="w-8 h-8 text-gray-400" />
                        </div>
                        <div className="text-center">
                            <p className="text-lg font-medium text-white">
                                Drag & drop your formatted data here
                            </p>
                            <p className="text-sm text-gray-400 mt-1">
                                Supports CSV, Excel, or PDF
                            </p>
                        </div>
                        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors pointer-events-none">
                            Browse Files
                        </button>
                    </>
                )}
            </div>

            {/* Simulation of Data Health Check */}
            {uploadedFile && (
                <div className="mt-6 bg-gray-900 border border-gray-700 rounded-lg p-4 animate-in fade-in slide-in-from-bottom-4">
                    <div className="flex items-center gap-3 mb-2">
                        <AlertCircle className="w-5 h-5 text-yellow-500" />
                        <h3 className="font-semibold text-white">Data Health Check</h3>
                        <span className="ml-auto text-sm text-green-400 font-mono">Score: 92/100</span>
                    </div>
                    <div className="space-y-2">
                        <div className="flex justify-between text-sm text-gray-400">
                            <span>Missing Values</span>
                            <span className="text-white">0%</span>
                        </div>
                        <div className="flex justify-between text-sm text-gray-400">
                            <span>Anomalies Detected</span>
                            <span className="text-yellow-400">3 rows corrected</span>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};
