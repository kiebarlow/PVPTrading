import React from "react";

function LeaderBoardEntry({ userName, profit, position }) {
  let borderColor = '';

  // Set the border color based on the position
  if (position === 1) {
    borderColor = 'border-[#C29A6A]'; // Muted gold color for 1st place
  } else if (position === 2) {
    borderColor = 'border-[#A3A3A3]'; // Muted silver color for 2nd place
  } else if (position === 3) {
    borderColor = 'border-[#5c472c]'; // Muted bronze color for 3rd place
  } else {
    borderColor = 'border-[#1E1E1E]'; // Default border color for others
  }

  return (
    <div className={`bg-[#0D0D0D] border ${borderColor} rounded-xl shadow-md p-4 w-full text-white text-sm flex flex-col md:flex-row items-center justify-between gap-4`}>
      <div className="text-lg font-semibold">{position}</div>
      <div className="text-gray-400">
        Name: {userName} <span className="text-white"></span>
      </div>
      <div className="text-gray-400">
        Total Profit: ${profit} <span className="text-white"></span>
      </div>
    </div>
  );
}

export default LeaderBoardEntry;