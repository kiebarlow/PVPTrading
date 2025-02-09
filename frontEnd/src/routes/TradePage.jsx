import React, { useState, useEffect } from "react";
import TradeView from "../components/tradePageComponents/TradeView";
import CustomizedSlider from "../components/tradePageComponents/LeverageSlider";
import WaitForGameStart from "../components/tradePageComponents/WaitForGameStart";

const INITIAL_BALANCE = 1000;
const CANDLE_COUNT = 25;
const CANDLE_INTERVAL = 60; // seconds
const PRICE_CHANGE_RANGE = 1000; // price fluctuation range

function TradePage() {
  const [chartData, setChartData] = useState([]);
  const [currentHoldings, setCurrentHoldings] = useState(0);
  const [balance, setBalance] = useState(INITIAL_BALANCE);
  const [waitingForGame, setWaitingForGame] = useState(true);
  const [tradeHistory, setTradeHistory] = useState([]);
  const [leverage, setLeverage] = useState(1);
  const [gameEnded, setGameEnded] = useState(false);
  const [tradeAmount, setTradeAmount] = useState("");
  const [activeOrders, setActiveOrders] = useState([]); // Track active positions
  const [markers, setMarkers] = useState([]); // Store trade markers for the chart

  const generateInitialData = () => {
    let startTime = Math.floor(Date.now() / 1000) - CANDLE_INTERVAL * CANDLE_COUNT;
    let price = 35000;
    return Array.from({ length: CANDLE_COUNT }, () => {
      const open = price;
      const close = open + (Math.random() - 0.5) * PRICE_CHANGE_RANGE;
      const high = Math.max(open, close) + Math.random() * 500;
      const low = Math.min(open, close) - Math.random() * 500;
      price = close;
      startTime += CANDLE_INTERVAL;
      return { time: startTime, open, close, high, low };
    });
  };

  const handleTradeExecution = (action) => {
    if (gameEnded) return;

    const amount = parseFloat(tradeAmount);
    if (!amount || amount <= 0 || amount > balance) {
      alert("Please enter a valid trade amount.");
      return;
    }

    const currentPrice = chartData[chartData.length - 1].close;
    const leverageAmount = amount * leverage;
    
    // Create new order
    const newOrder = {
      id: Date.now(),
      action,
      amount: leverageAmount,
      entryPrice: currentPrice,
      time: new Date().toLocaleTimeString()
    };

    setActiveOrders(prev => [...prev, newOrder]);
    setBalance(prev => prev - amount);
    setCurrentHoldings(prev => prev + (action === "long" ? leverageAmount : -leverageAmount));

    // Add marker to chart
    const newMarker = {
      time: chartData[chartData.length - 1].time,
      position: action === "long" ? "belowBar" : "aboveBar",
      color: action === "long" ? "#22c55e" : "#dc2626",
      shape: action === "long" ? "arrowUp" : "arrowDown",
      text: `${action.toUpperCase()} $${amount}`
    };
    setMarkers(prev => [...prev, newMarker]);

    // Add to trade history
    setTradeHistory(prev => [
      ...prev,
      {
        action,
        amount,
        price: currentPrice,
        profitLoss: 0,
        time: new Date().toLocaleTimeString()
      }
    ]);
  };

  const closePosition = (orderId) => {
    const order = activeOrders.find(o => o.id === orderId);
    if (!order) return;

    const currentPrice = chartData[chartData.length - 1].close;
    const priceDiff = currentPrice - order.entryPrice;
    const profitLoss = order.action === "long" ? 
      priceDiff * order.amount : 
      -priceDiff * order.amount;

    // Update balance and holdings
    setBalance(prev => prev + (order.amount / leverage) + profitLoss);
    setCurrentHoldings(prev => prev - (order.action === "long" ? order.amount : -order.amount));

    // Add close marker to chart
    const newMarker = {
      time: chartData[chartData.length - 1].time,
      position: order.action === "long" ? "aboveBar" : "belowBar",
      color: profitLoss >= 0 ? "#22c55e" : "#dc2626",
      shape: "circle",
      text: `CLOSE ${order.action.toUpperCase()} P/L: $${profitLoss.toFixed(2)}`
    };
    setMarkers(prev => [...prev, newMarker]);

    // Update trade history
    setTradeHistory(prev => [
      ...prev,
      {
        action: `close_${order.action}`,
        amount: order.amount / leverage,
        price: currentPrice,
        profitLoss,
        time: new Date().toLocaleTimeString()
      }
    ]);

    // Remove from active orders
    setActiveOrders(prev => prev.filter(o => o.id !== orderId));
  };

  useEffect(() => {
    const data = generateInitialData();
    setChartData(data);

    const interval = setInterval(() => {
      setChartData((prevData) => {
        const lastCandle = prevData[prevData.length - 1];
        const newTime = lastCandle.time + CANDLE_INTERVAL;
        const open = lastCandle.close;
        const close = open + (Math.random() - 0.5) * PRICE_CHANGE_RANGE;
        const high = Math.max(open, close) + Math.random() * 500;
        const low = Math.min(open, close) - Math.random() * 500;
        return [...prevData.slice(1), { time: newTime, open, close, high, low }];
      });
    }, 100);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="h-screen bg-[#0D0D0D] text-white flex flex-col p-6">
      <WaitForGameStart isOpen={false} />
      <header className="p-4 border-b border-gray-800">
        <h1 className="text-4xl font-bold">BTC/USDT</h1>
      </header>
      <main className="flex-grow flex overflow-hidden">
        <div className="flex-1 h-full">
          <TradeView data={chartData} markers={markers} />
        </div>
        <div className="w-[20%] p-4 flex flex-col space-y-4 border-l border-gray-800 items-center text-center overflow-y-auto">
          <h3>Current Position: {currentHoldings}</h3>
          <h3>Balance: ${balance.toFixed(2)}</h3>
          <input
            type="number"
            placeholder="Amount ($)"
            value={tradeAmount}
            onChange={(e) => setTradeAmount(e.target.value)}
            className="bg-gray-800 text-white p-2 rounded w-full"
          />
          <button
            className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded w-full"
            onClick={() => handleTradeExecution("long")}
          >
            Long
          </button>
          <button
            className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded w-full"
            onClick={() => handleTradeExecution("short")}
          >
            Short
          </button>
          <div className="mt-0 w-full">
            <h3 className="text-lg font-semibold mb-2">Leverage</h3>
            <CustomizedSlider value={leverage} onChange={setLeverage} />
          </div>
          
          {/* Active Positions Section */}
          <div className="mt-0 w-full">
            <h3 className="text-lg font-semibold mb-2">Active Positions</h3>
            <div className="space-y-2">
              {activeOrders.map((order) => {
                const currentPrice = chartData[chartData.length - 1].close;
                const priceDiff = currentPrice - order.entryPrice;
                const unrealizedPL = order.action === "long" ? 
                  priceDiff * order.amount : 
                  -priceDiff * order.amount;
                
                return (
                  <div key={order.id} className="bg-gray-800 p-2 rounded">
                    <div className="flex justify-between items-center">
                      <span>{order.action.toUpperCase()}</span>
                      <span className={unrealizedPL >= 0 ? "text-green-500" : "text-red-500"}>
                        ${unrealizedPL.toFixed(2)}
                      </span>
                    </div>
                    <button
                      onClick={() => closePosition(order.id)}
                      className="bg-yellow-600 hover:bg-yellow-700 text-white font-bold py-1 px-2 rounded mt-2 w-full"
                    >
                      Close Position
                    </button>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="mt-0 w-full">
            <h3 className="text-lg font-semibold mb-2">Trade History</h3>
            <ul className="text-left space-y-2">
              {tradeHistory.map((trade, index) => (
                <li key={index} className="text-sm">
                  <strong>{trade.action.toUpperCase()}</strong> - ${trade.amount} at {trade.price} | P/L: ${trade.profitLoss.toFixed(2)} | {trade.time}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </main>
    </div>
  );
}

export default TradePage;