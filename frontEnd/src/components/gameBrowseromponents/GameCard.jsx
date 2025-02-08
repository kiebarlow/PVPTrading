import React from 'react'

function gameCard({entryFee, numPlayers, timeToStart}) {
  return (
    <div className="bg-[#0D0D0D] border border-[#1E1E1E] rounded-xl shadow-md p-4 w-64 text-white text-sm flex flex-col gap-2">
      <div className="text-lg font-semibold">{entryFee} Gems</div>
      <div className="text-gray-400">Number of players: <span className="text-white">{numPlayers}</span></div>
      <div className="text-gray-400">Time till start: <span className="text-white">{timeToStart}</span></div>
      <button className="mt-2 bg-green-600 hover:bg-green-700 text-white font-medium py-1.5 rounded-lg transition">
        Join Game
      </button>
    </div>

    
  )
}

export default gameCard