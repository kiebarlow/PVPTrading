import { create } from "zustand";
const apiUrl = 'http://127.0.0.1:5000';
import { sha256 } from "crypto-hash";

export const useStore = create((set, get) => ({
    userId: null,  // Added userId state
    userDepositAddress: null,
    userGemBalance: 0,

    register: async (userName, password) => {
        const hashedPassword = await sha256(password); // Hash password
        const response = await fetch(`${apiUrl}/registerUser`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ userName, password: hashedPassword }),
        });
        return response.json();
      },
    
      login: async (userName, password) => {
        const hashedPassword = await sha256(password); // Hash password
        const response = await fetch(`${apiUrl}/loginUser`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ userName, password: hashedPassword }),
        });
        return response.json();
      },

  
    checkForDeposit: async (userId) => {
      const response = await fetch(`${apiUrl}/checkForDeposit`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json'},
        mode: 'no-cors',
        body: JSON.stringify({ userId })
      });
      return response.json();
    },
  }));

export default useStore;

