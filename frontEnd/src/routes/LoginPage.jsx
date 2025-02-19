import React, { useState } from "react";
import useStore from "../UseStore";
function LoginPage() {
  const [isRegister, setIsRegister] = useState(false);
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const { register, login } = useStore();

  

  const handleAuth = async () => {
    if (isRegister) {
      if (password !== confirmPassword) {
        alert("Passwords do not match");
        return;
      }
      const response = await register(userName, password);
      console.log("Register response:", response);
    } else {
      const response = await login(userName, password);
      console.log("Login response:", response);
    }
  };

  return (
    <div className="min-h-screen bg-[#0D0D0D] text-white p-8 flex flex-col justify-center items-center">
      <div className="bg-[#1E1E1E] p-6 rounded-lg shadow-md w-full max-w-sm">
        <h2 className="text-2xl font-bold text-center mb-4">
          {isRegister ? "Register" : "Login"}
        </h2>
        <div className="space-y-4">
          <input
            type="text"
            placeholder="Username"
            className="w-full p-2 bg-gray-800 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            value={userName}
            onChange={(e) => setUserName(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            className="w-full p-2 bg-gray-800 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {isRegister && (
            <input
              type="password"
              placeholder="Confirm Password"
              className="w-full p-2 bg-gray-800 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
          )}
          <button
            className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 rounded-md transition"
            onClick={handleAuth}
          >
            {isRegister ? "Register" : "Login"}
          </button>
        </div>
        <div className="mt-4 text-center text-sm">
          {isRegister ? "Already have an account?" : "Don't have an account?"}
          <button
            onClick={() => setIsRegister(!isRegister)}
            className="text-green-400 hover:underline ml-1"
          >
            {isRegister ? "Login" : "Register"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
