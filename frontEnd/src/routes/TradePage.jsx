import React, { useState, useEffect } from "react";
import TradeView from "../components/tradePageComponents/TradeView";
import CustomizedSlider from "../components/tradePageComponents/LeverageSlider";
import WaitForGameStart from "../components/tradePageComponents/WaitForGameStart";
import GameResults from "../components/tradePageComponents/GameResults";

function TradePage() {
  const [chartData, setChartData] = useState([]);
  const currentHoldings = 500;
  const [waitingForGame, setWaitingForGame] = useState(false);
  const [showResults, setShowResults] = useState(false);
  // connect above to backend

  useEffect(() => {
    const data = [
      { time: 1625097600, open: 35000, close: 35500, high: 35700, low: 34900 },
      { time: 1625101200, open: 35500, close: 35300, high: 35600, low: 35200 },
    
      //HERE WE NEED TO CONECT SOCKET AND THEN WHEN START GAME EMISSON RECIEVED SET waitingForGame to false

    ];

    setChartData(data);
  }, []); // Empty dependency array to ensure this runs only once when the component mounts

  return (
    <div className="h-screen bg-[#0D0D0D] text-white flex flex-col p-6">
      <WaitForGameStart isOpen={waitingForGame} />
      <GameResults isOpen={showResults} />
      <header className="p-4 border-b border-gray-800">
        <h1 className="text-4xl font-bold">BTC/USDT</h1>
      </header>
      <main className="flex-grow flex overflow-hidden">
        
        {/* Trading View Container */}
        <div className="flex-1 h-full">
          <TradeView data={chartData} />
        </div>

        {/* Side Panel */}
        <div className="w-[20%] p-4 flex flex-col space-y-4 border-l border-gray-800 items-center text-center overflow-y-auto">
          <h3>Current Position: {currentHoldings}</h3>
          <input
            type="number"
            placeholder="Amount ($)"
            className="bg-gray-800 text-white p-2 rounded w-full"
          />
          <button className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded w-full">
            Long
          </button>
          <button className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded w-full">
            Short
          </button>
          <div className="mt-0 w-full">
            <h3 className="text-lg font-semibold mb-2">Leverage</h3>
            <CustomizedSlider />
          </div>
          <button className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded w-full">
            Buy A Tree
          </button>
          <div className="mt-0 w-full">
            <h3 className="text-lg font-semibold mb-2">Trade History</h3>
            {/* Add order book content here */}
          </div>
        </div>
      </main>
    </div>
  );
}

export default TradePage;
