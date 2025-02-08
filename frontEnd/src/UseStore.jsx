import { create } from "zustand";
import { sha256 } from "crypto-hash";
import { io } from "socket.io-client";

const apiUrl = "http://127.0.0.1:5000";

export const useStore = create((set, get) => ({
  userId: null, // Added userId state
  userDepositAddress: null,
  userGemBalance: 0,
  socketData: [],
  tickerData: [],

  setTickerData: (data) => set({ tickerData: data }),

  // Initialize the socket connection
  connect: (url) => {
    const socket = io(url);

    socket.on("connect", () => {
      console.log("Connected to socket.io server");
      set({ socket });
    });

    socket.on("historicalData", (message) => {
      console.log("Received historical data, updating tickerData...");
      set({ tickerData: message });
    });

    set({ socket });
  },

  // Function to send data to the backend via socket
  sendData: async (event, message) => {
    const { socket } = get();
    if (socket) {
      socket.emit(event, message);
      console.log(`Emitted message to event ${event}:`, message);
    } else {
      console.error("Socket is not connected.");
    }
  },

  // Register a new user
  register: async (userName, password) => {
    const hashedPassword = await sha256(password); // Hash password
    const response = await fetch(`${apiUrl}/registerUser`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ userName, password: hashedPassword }),
    });
    return response.json();
  },

  // Log in the user
  login: async (userName, password) => {
    const hashedPassword = await sha256(password); // Hash password
    const response = await fetch(`${apiUrl}/loginUser`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ userName, password: hashedPassword }),
    });
    return response.json();
  },

  // Check if user has a deposit
  checkForDeposit: async (userId) => {
    const response = await fetch(`${apiUrl}/checkForDeposit`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ userId }),
    });
    return response.json();
  },
}));

export default useStore;