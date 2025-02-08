import React, { useState, useEffect } from 'react';
import TradeView from '../components/tradePageComponents/TradeView';
import CustomizedSlider from '../components/tradePageComponents/LeverageSlider';

function TradePage() {
  const [chartData, setChartData] = useState([]);
  const currentHoldings = 500
  // connect above to backend 

  useEffect(() => {
    const data = [
        { time: 1625097600, open: 35000, close: 35500, high: 35700, low: 34900 },
        { time: 1625101200, open: 35500, close: 35300, high: 35600, low: 35200 },
        { time: 1625104800, open: 35300, close: 35400, high: 35500, low: 35250 },
        { time: 1625108400, open: 35400, close: 35800, high: 36000, low: 35300 },
        { time: 1625112000, open: 35800, close: 35600, high: 35900, low: 35450 },
        { time: 1625115600, open: 35600, close: 35700, high: 35850, low: 35500 },
        { time: 1625119200, open: 35700, close: 36000, high: 36200, low: 35650 },
        { time: 1625122800, open: 36000, close: 35900, high: 36100, low: 35800 },
        { time: 1625126400, open: 35900, close: 36200, high: 36400, low: 35850 },
        { time: 1625130000, open: 36200, close: 36300, high: 36500, low: 36100 },
        { time: 1625133600, open: 36300, close: 36500, high: 36700, low: 36250 },
        { time: 1625137200, open: 36500, close: 36600, high: 36800, low: 36400 },
        { time: 1625140800, open: 36600, close: 36800, high: 37000, low: 36550 },
        { time: 1625144400, open: 36800, close: 37000, high: 37200, low: 36650 },
        { time: 1625148000, open: 37000, close: 37200, high: 37400, low: 36800 },
        { time: 1625151600, open: 37200, close: 37100, high: 37350, low: 36950 },
        { time: 1625155200, open: 37100, close: 37300, high: 37500, low: 36900 },
        { time: 1625158800, open: 37300, close: 37500, high: 37650, low: 37150 },
        { time: 1625162400, open: 37500, close: 37700, high: 37900, low: 37350 },
        { time: 1625166000, open: 37700, close: 37800, high: 38000, low: 37450 },
        { time: 1625169600, open: 37800, close: 38000, high: 38150, low: 37600 },
        { time: 1625173200, open: 38000, close: 38200, high: 38400, low: 37750 },
        { time: 1625176800, open: 38200, close: 38300, high: 38500, low: 37900 },
        { time: 1625180400, open: 38300, close: 38500, high: 38700, low: 38050 },
        { time: 1625184000, open: 38500, close: 38600, high: 38800, low: 38150 },
        
      ];
      
    setChartData(data);
  }, []);  // Empty dependency array to ensure this runs only once when the component mounts

  return (
    <div className="h-screen bg-[#0D0D0D] text-white flex flex-col">
      <header className="p-4 border-b border-gray-800">
        <h1 className="text-4xl font-bold">BTC/USDT</h1>
      </header>
      <main className="flex-grow flex overflow-hidden">
        <div className="w-[80%] h-[90%]">
          <TradeView data={chartData} />
        </div>
        <div className="w-[20%] p-4 flex flex-col space-y-4 border-l border-gray-800 items-center text-center">
        <h3>Current Position: {currentHoldings}</h3>
        <input
          type="number"
          placeholder="Amount ($)"
          className="bg-gray-800 text-white p-2 rounded w-96"
        />
        <button className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded w-96">
          Long
        </button>
        <button className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded w-96">
          Short
        </button>
        <div className="mt-0">
          <h3 className="text-lg font-semibold mb-2">Leverage</h3>
          <CustomizedSlider />
        </div>
        <button className="bg-blue-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
          Buy A Tree
        </button>
        <div className="mt-0">
          <h3 className="text-lg font-semibold mb-2">Trade History</h3>
          {/* Add order book content here */}
        </div>
      </div>
      </main>
    </div>
  );
}

export default TradePage;