import React from 'react';

function PreviousGameCard({ prizePool, numPlayers, dateFinish }) {
  return (
    <div className="bg-[#0D0D0D] border border-[#1E1E1E] rounded-xl shadow-md p-4 w-full text-white text-sm flex flex-col md:flex-row items-center justify-between gap-4">
      <div className="text-lg font-semibold">Prize Pool: ${prizePool}</div>
      <div className="text-gray-400">Number of Players: <span className="text-white">{numPlayers}</span></div>
      <div className="text-gray-400">Date: <span className="text-white">{dateFinish}</span></div>
    </div>
  );
}

export default PreviousGameCard;