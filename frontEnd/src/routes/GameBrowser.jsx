import React, { useState } from "react";
import GameCard from "../components/gameBrowseromponents/gameCard";
import PreviousGameCard from "../components/gameBrowseromponents/PreviousGameCard";
import axios from "axios";
import Cookies from "js-cookie";
import { useNavigate } from "react-router"

function GameBrowser() {
  const [entryCost, setEntryCost] = useState("");
  const navigate = useNavigate();

  const createGame = async () => {
    if (!entryCost) {
      console.error("Entry cost is required");
      return;
    }

    try {
      const response = await axios.post(
        "/api/createGame", // Proxy should redirect this to backend
        { userName: Cookies.get("userName"), entryCost: parseFloat(entryCost) },  // Replace with actual user data
        {
          headers: { "Content-Type": "application/json" },
          withCredentials: true, // If using cookies
        }
      );
      console.log("Game created:", response.data);
      //NAvigates to the trade page
      navigate('/TradePage')
      return response.data;
    } catch (error) {
      console.error("Game creation error:", error.response?.data?.message || "An error occurred");
    }
  };

  return (
    <div className="min-h-screen bg-[#0D0D0D] text-white p-8">
      <div className="mb-6">
        <h1 className="text-4xl font-bold">Create Game</h1>
      </div>

      <div className="mb-10">
        <h1 className="text-6xl font-semibold mb-4 CPMono">Live Games</h1>
        <div className="flex flex-wrap gap-5">
          <div className="flex flex-row overflow-x-auto space-x-4 w-full">
            <div className="bg-[#0D0D0D] border border-[#1E1E1E] rounded-xl shadow-md p-4 w-64 text-white text-sm flex flex-col gap-2">
              <input
                type="number"
                placeholder="Enter price"
                className="bg-gray-800 text-white p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={entryCost}
                onChange={(e) => setEntryCost(e.target.value)}
              />
              <button
                className="mt-2 bg-blue-600 hover:bg-blue-700 text-white font-medium py-1.5 rounded-lg transition"
                onClick={createGame} // Pass function reference, don't call it immediately
              >
                Create Game
              </button>
            </div>

            <GameCard entryFee={10} numPlayers={2} timeToStart={10} />
            <GameCard entryFee={20} numPlayers={4} timeToStart={5} />
            <GameCard entryFee={15} numPlayers={3} timeToStart={8} />
          </div>
        </div>
      </div>

      <div className="flex flex-col justify-evenly">
        <h1 className="text-6xl font-semibold mb-4">Previous Games</h1>

        <PreviousGameCard prizePool={500} numPlayers={12} dateFinish={"12 Jan"} />
        <PreviousGameCard prizePool={500} numPlayers={12} dateFinish={"12 Jan"} />
        <PreviousGameCard prizePool={500} numPlayers={12} dateFinish={"12 Jan"} />
      </div>
    </div>
  );
}

export default GameBrowser;