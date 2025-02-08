import React, { useState, useEffect } from "react";
import TradeView from "../components/tradePageComponents/TradeView";
import CustomizedSlider from "../components/tradePageComponents/LeverageSlider";
import WaitForGameStart from "../components/tradePageComponents/WaitForGameStart";
import io from 'socket.io-client'

function TradePage() {
  const [chartData, setChartData] = useState([]);
  const currentHoldings = 500;
  const [waitingForGame, setWaitingForGame] = useState(false);
  const [tradePair, setTradePair] = useState("SOLUSDT")
  const [tradeAmount, setTradeAmount] = useState() // amount in the text field may need a better name!
  const [leverageAmount, setLeverageAmount] = useState(100)
  const userID = 12345

  const socket = io('http://localhost:5000',{
    transports: ['websocket']
  })

  const switchPair = (newPair) => { // not working rn
    setTradePair(newPair);
    console.log(newPair)
    socket.emit('historicalDataRequest',newPair)
  }

  const tradeToken = (amount,leverage,pair) => {
    console.log({margin: amount, leverage: leverage, pair: pair, userID: userID})
    socket.emit('long',{amount: amount, pair: pair, userID: userID}) // negative amount values = selling or shorting
  }

  // Request historical data when tradePair changes
  useEffect(() => {
    console.log("Requesting historical data for:", tradePair);
    socket.emit("historicalDataRequest", tradePair);

    // Listen for historical data
    const historicalDataListener = (data) => {
      console.log("Historical data received:", data);
      setChartData(data);
    };

    socket.on("historicalData", historicalDataListener);

    return () => {
      socket.off("historicalData", historicalDataListener); // Cleanup listener
    };
  }, [tradePair]); // ✅ Runs every time tradePair changes

  useEffect(() => {

    socket.emit('historicalDataRequest', tradePair)
    console.log("requesting data")

    socket.on('historicalData', (data) => {
        console.log(data)
        //add data processing
        setChartData(data)
        console.log("historical data received")
    })
    


    socket.on('newCandle', (data) => {
        //add data processing
        console.log(data)
        console.log(tradePair)
        setChartData((prevData) => {
            let newTime = data[tradePair].time;
            let open = prevData[prevData.length - 1].close;
            let close = data[tradePair].close;
            let high = data[tradePair].high;
            let low = data[tradePair].low;
    
            // Append new candle and remove oldest one
            if (prevData.length > 500) {
                return [...prevData.slice(1), { time: newTime, open, close, high, low }];
            }
            return [...prevData, { time: newTime, open, close, high, low }];
            });
    })

  }, []); // Empty dependency array to ensure this runs only once when the component mounts

   

  return (
    <div className="h-screen bg-[#0D0D0D] text-white flex flex-col p-6">
      <WaitForGameStart isOpen={waitingForGame} />
      <header className="p-4 border-b border-gray-800">
        <div className="flex justify-between space-x-4">
            <button className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded w-full" onClick={() => switchPair("BTCUSDT")}>BTC/USDT</button>
            <button className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded w-full" onClick={() => switchPair("SOLUSDT")}>SOL/USDT</button>
            <button className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded w-full" onClick={() => switchPair("ETHUSDT")}>ETH/USDT</button>
        </div>
      </header>
      <main className="flex-grow flex overflow-hidden">
        
        {/* Trading View Container */}
        <div className="flex-1 h-full">
          <TradeView data={chartData} />
        </div>

        {/* Side Panel */}
        <div className="w-[20%] p-4 flex flex-col space-y-4 border-l border-gray-800 items-center text-center overflow-y-auto">
          <h3>Current Position Value: {currentHoldings}</h3>
          <input
            value={tradeAmount}
            onChange={(event) => {setTradeAmount(event.target.value)}}
            type="number"
            placeholder="Amount ($)"
            className="bg-gray-800 text-white p-2 rounded w-full"
          />
          <button className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded w-full" onClick={() => tradeToken(tradeAmount, leverageAmount,tradePair)}>
            Long
          </button>
          <button className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded w-full" onClick={() => tradeToken(tradeAmount * -1, leverageAmount,tradePair)}>
            Short
          </button> 
          <div className="mt-0 w-full">
            <h3 className="text-lg font-semibold mb-2">Leverage</h3>
            <CustomizedSlider onChange={(newValue) => {setLeverageAmount(newValue)}} />
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
