import React from 'react'

function WaitForGameStart({isOpen}) {
    if (!isOpen) return null;
    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-gray-800 p-8 rounded-lg shadow-xl flex flex-col items-center">
 
            <h2 className="text-2xl font-bold text-white mb-4">Waiting for Game to Start</h2>
            <p className="text-gray-300 text-center mb-4">
              Number Of Players:
            </p>
            <p className="text-gray-300 text-center mb-4">
              Time To Start:
            </p>
            <div className="flex gap-2">
              <div className="h-2 w-2 bg-blue-500 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
              <div className="h-2 w-2 bg-blue-500 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
              <div className="h-2 w-2 bg-blue-500 rounded-full animate-bounce"></div>
            </div>
          </div>
        </div>
      );
    };

export default WaitForGameStart