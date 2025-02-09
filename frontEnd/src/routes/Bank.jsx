import React, { useState } from "react";
import Cookies from "js-cookie";
import { useStore } from "../UseStore";

function Bank() {
  const [depositPageSelected, setDepositPageSelected] = useState(true);
  const [solanaAddress, setSolanaAddress] = useState("");
  const [gems, setGems] = useState("");
  const [cookieGems, setCookieGems] = useState(Cookies.get("gems") || "");

  const handleWithdraw = () => {
    console.log("Solana Address:", solanaAddress);
    console.log("Number of Gems:", gems);
  };

  const handleSetCookie = () => {
    Cookies.set("gems", cookieGems);
    window.location.reload();
  };

  return (
    <div className="min-h-screen bg-[#0D0D0D] text-white p-8 flex flex-col justify-center items-center">
      <h1 className="text-3xl font-semibold mb-6">
        Gems: {Cookies.get("gems") || 0}
      </h1>
      <h1 className="text-3xl font-semibold mb-6">1 Solana = 1000 Gems</h1>

      {/* Set Gems Cookie */}
      <div className="mb-6 flex flex-col items-center">
        <input
          type="number"
          placeholder="Set Gems"
          value={cookieGems}
          onChange={(e) => setCookieGems(e.target.value)}
          className="w-full p-3 mb-2 text-xl font-mono bg-[#333333] text-white rounded-lg"
        />
        <button
          onClick={handleSetCookie}
          className="py-2 px-6 bg-green-600 hover:bg-green-700 rounded-lg"
        >
          Set Gems
        </button>
      </div>

      {/* Tab Navigation */}
      <div className="flex space-x-6 mb-8">
        <button
          onClick={() => setDepositPageSelected(true)}
          className={`py-2 px-6 rounded-lg transition-colors duration-200 ${
            depositPageSelected ? "bg-green-600" : "bg-[#333333]"
          } hover:bg-green-700`}
        >
          Deposit
        </button>
        <button
          onClick={() => setDepositPageSelected(false)}
          className={`py-2 px-6 rounded-lg transition-colors duration-200 ${
            !depositPageSelected ? "bg-green-600" : "bg-[#333333]"
          } hover:bg-green-700`}
        >
          Withdraw
        </button>
      </div>

      {/* Content */}
      {!depositPageSelected && (
        <div className="text-center">
          <div className="text-lg font-semibold mb-4">Withdraw</div>
          <div className="bg-[#1A1A1A] p-6 rounded-lg">
            <p className="text-sm opacity-70 mb-4">
              Enter your Solana address and the number of gems to withdraw:
            </p>

            <input
              type="text"
              placeholder="Input Solana address"
              value={solanaAddress}
              onChange={(e) => setSolanaAddress(e.target.value)}
              className="w-full p-3 mb-4 text-xl font-mono bg-[#333333] text-white rounded-lg"
            />

            <input
              type="number"
              placeholder="Number of gems"
              value={gems}
              onChange={(e) => setGems(e.target.value)}
              className="w-full p-3 mb-4 text-xl font-mono bg-[#333333] text-white rounded-lg"
            />

            <button
              onClick={handleWithdraw}
              className="w-full py-3 mt-4 bg-blue-600 text-white rounded-lg"
            >
              Withdraw (0.5 SOL)
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Bank;
