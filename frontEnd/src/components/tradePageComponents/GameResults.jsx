import React from "react";

function GameResults({ isOpen }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-800 p-8 rounded-lg shadow-xl flex flex-col items-center w-80">
        <h2 className="text-2xl font-bold text-white mb-4">🎉 You Won! 🎉</h2>

        <p className="text-gray-300 text-center mb-2">
          Total Profit: <span className="text-white font-bold">$59,931,923</span>
        </p>

        <p className="text-gray-300 text-center mb-2">
          Gems Won: <span className="text-white font-bold">400</span>
        </p>

        {/* Podium */}
        <div className="relative w-full flex justify-center items-end h-40 mt-4">
          {/* 🥈 Second Place */}
          <div className="bg-gray-600 h-16 w-14 rounded-t-lg flex flex-col items-center">
            <span className="text-lg">🥈</span>
            <span className="text-sm text-gray-300">Player 2</span>
            <span className="text-xs text-gray-400">2300 pts</span>
          </div>

          {/* 🥇 First Place (Taller Podium) */}
          <div className="bg-yellow-500 h-24 w-16 mx-2 rounded-t-lg flex flex-col items-center">
            <span className="text-2xl">🥇</span>
            <span className="text-md text-black font-bold">You</span>
            <span className="text-sm text-gray-800">2500 pts</span>
          </div>

          {/* 🥉 Third Place */}
          <div className="bg-gray-700 h-12 w-14 rounded-t-lg flex flex-col items-center">
            <span className="text-lg text-white">🥉</span>
            <span className="text-sm text-gray-300">Player 3</span>
            <span className="text-xs text-gray-400">1800 pts</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default GameResults;