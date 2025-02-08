import React from "react";
import GameCard from "../components/gameBrowseromponents/gameCard";
import PreviousGameCard from "../components/gameBrowseromponents/PreviousGameCard";
import { FaRegGem } from "react-icons/fa6";
function GameBrowser() {
  return (
    <div className="min-h-screen bg-[#0D0D0D] text-white p-8">
      <div className="mb-6">
        <h1 className="text-4xl font-bold">Create Game</h1>
      </div>

      <div className="mb-10">
        <h1 className="text-6xl font-semibold mb-4 CPMono">Live Games</h1>
        <div className="flex flex-wrap gap-5">
          <div className="bg-[#0D0D0D] border border-[#1E1E1E] rounded-xl shadow-md p-4 w-64 text-white text-sm flex flex-col gap-2">
            <div className="text-lg font-semibold">Entry Price:</div>
            <button className="mt-2 bg-blue-600 hover:bg-green-700 text-white font-medium py-1.5 rounded-lg transition">
              Create Game
            </button>
          </div>
          <GameCard entryFee={10} numPlayers={2} timeToStart={10} />
          <GameCard entryFee={20} numPlayers={4} timeToStart={5} />
          <GameCard entryFee={15} numPlayers={3} timeToStart={8} />
        </div>
      </div>

      <div className="flex flex-col justify-evenly">
        <h1 className="text-6xl font-semibold mb-4">Previous Games</h1>

        <PreviousGameCard
          prizePool={500}
          numPlayers={12}
          dateFinish={"12 Jan"}
        />
        <PreviousGameCard
          prizePool={500}
          numPlayers={12}
          dateFinish={"12 Jan"}
        />

        <PreviousGameCard
          prizePool={500}
          numPlayers={12}
          dateFinish={"12 Jan"}
        />
      </div>
    </div>
  );
}

export default GameBrowser;
