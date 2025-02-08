export default function Header() {
    return (
      <header className="bg-gradient-to-b from-black to-[#0a1f0b] p-4 shadow-md flex justify-between items-center">
        {/* Logo */}
        <div className="text-white text-xl font-bold tracking-wide">
          PVPTrading.<span className="text-blue-500">Club</span>
        </div>
        
        {/* Navigation */}
        <nav className="hidden md:flex space-x-6 text-gray-300 text-sm font-medium">
          <span className="hover:text-white transition">Browse Games</span>
          <span className="hover:text-white transition">Leaderboard</span>
          <span className="hover:text-white transition">Bank</span>
        </nav>
        
        {/* Connect Wallet Placeholder */}
        <span className="bg-blue-600 text-white px-4 py-2 rounded-lg shadow-md">Connect Wallet</span>
      </header>
    );
  }
  