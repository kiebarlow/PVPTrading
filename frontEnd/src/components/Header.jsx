import { useState, useEffect } from "react";
import { Outlet, Link } from "react-router-dom";
import { FaPiggyBank, FaTrophy, FaHouse, FaGem } from "react-icons/fa6";
import Cookies from "js-cookie";
import { useNavigate } from "react-router";

export default function Header() {
  const [userName, setUserName] = useState(Cookies.get("userName") || null);
  const navigate = useNavigate();

  useEffect(() => {
    const interval = setInterval(() => {
      const newUser = Cookies.get("userName") || null;
      if (newUser !== userName) {
        setUserName(newUser);
      }
    }, 1000); // Check every second (adjust as needed)

    return () => clearInterval(interval); // Cleanup interval on unmount
  }, [userName]);

  return (
    <header className="bg-gradient-to-b from-black to-[#0a1f0b] p-4 shadow-md flex justify-between items-center">
      {/* Logo */}
      <div className="text-white text-xl font-bold tracking-wide">
        PVPTrading.<span className="text-green-500">Club</span>
      </div>

      {/* Navigation */}
      <nav className="hidden md:flex space-x-6 text-gray-300 text-sm font-medium">
        <Link to="browseGames" className="flex items-center space-x-2">
          <div className="text-lg font-semibold">Browse Games</div>
          <FaHouse className="text-xl" />
        </Link>

        <Link to="leaderBoard" className="flex items-center space-x-2">
          <div className="text-lg font-semibold">Leaderboard</div>
          <FaTrophy className="text-xl" />
        </Link>

        <Link to="bank" className="flex items-center space-x-2">
          <div className="text-lg font-semibold">Bank</div>
          <FaPiggyBank className="text-xl" />
        </Link>
      </nav>

      {/* Dynamic Login/Logout */}
      {userName ? (
        <span
          className="bg-green-600 text-white px-4 py-2 rounded-lg shadow-md cursor-pointer"
          onClick={() => {
            navigate("/bank");
          }}
        >
          <div className="flex items-center space-x-2">
            <div>{Cookies.get("gems")}</div>
            <FaGem />
          </div>
        </span>
      ) : (
        <span className="bg-green-600 text-white px-4 py-2 rounded-lg shadow-md">
          <Link to="loginRegister">Login</Link>
        </span>
      )}
    </header>
  );
}
