import React, { useState, useEffect } from "react";
import useStore from "../UseStore";
import TradeView from "../components/tradePageComponents/TradeView";
import CustomizedSlider from "../components/tradePageComponents/LeverageSlider";
import WaitForGameStart from "../components/tradePageComponents/WaitForGameStart";

function TradePage() {
  const [chartData, setChartData] = useState([]);
  const currentHoldings = 500;
  const [waitingForGame, setWaitingForGame] = useState(false);

  // Accessing store states and actions
  const sendData = useStore((state) => state.sendData);
  const solData = useStore((state) => state.solData);

  useEffect(() => {
    // Trigger WebSocket request for historical data when page loads (only once)
    const generateInitialData = async () => {
      sendData("historicalDataRequest", "SOLUSDT");
    };
  
    // Call generateInitialData only once
    generateInitialData();
  
  }, []); // Empty dependency array ensures this runs only once when the component mounts
  
  useEffect(() => {
    // Update chart data whenever solData changes
    if (solData.length > 0) {
      setChartData(solData); // Use the updated solData for chart
    } else {
      // If no solData, use fallback data
      const fallbackData = generateFallbackData();
      setChartData(fallbackData);
    }
  }, [solData]); // Dependency on solData for re-renders

  // Generate fallback data if no data is set
  const generateFallbackData = () => {
    let startTime = Math.floor(Date.now() / 1000) - 3600; // Start 1 hour ago
    let price = 35000;

    return new Array(25).fill(0).map(() => {
      let open = price;
      let close = open + (Math.random() - 0.5) * 1000; // Random close
      let high = Math.max(open, close) + Math.random() * 500;
      let low = Math.min(open, close) - Math.random() * 500;

      price = close; // Next open price is the last close price
      startTime += 60; // Increment time (1 minute interval)

      return { time: startTime, open, close, high, low };
    });
  };

  return (
    <div className="h-screen bg-[#0D0D0D] text-white flex flex-col p-6">
      <WaitForGameStart isOpen={waitingForGame} />
      <header className="p-4 border-b border-gray-800">
        <h1 className="text-4xl font-bold">SOL/USDT</h1>
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