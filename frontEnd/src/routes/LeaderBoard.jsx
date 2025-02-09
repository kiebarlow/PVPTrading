import React, { useState } from "react";
import StatCard from "../components/leaderBoard/StatCard";
import LeaderBoardEntry from "../components/leaderBoard/LeaderBoardEntry";

function LeaderBoard() {
  const [leaderboardData, setLeaderboardData] = useState([
    { position: 1, username: "seb", profit: "1232134" },
    { position: 2, username: "alex", profit: "876543" },
    { position: 3, username: "john", profit: "345678" },
    { position: 4, username: "jane", profit: "345678" },
    { position: 5, username: "david", profit: "987654" },
  ]);

  return (
    <div className="min-h-screen bg-[#0D0D0D] text-white p-8">
      <div className="flex flex-row">
        <StatCard />
        <StatCard />
      </div>
      <div className="flex flex-col justify-center">
        <div className="text-2xl font-semibold mb-4 text-center">
          Leader Board
        </div>
        <div className="max-w-3xl mx-auto p-4 bg-black min-h-screen">
          {leaderboardData.map((entry, index) => (
            <LeaderBoardEntry
              position={entry.position}
              userName={entry.username}
              profit={entry.profit}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

export default LeaderBoard;
