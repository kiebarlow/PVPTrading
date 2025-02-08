import React from "react";
import ReactDOM from "react-dom/client";

import './index.css'


import { createBrowserRouter, RouterProvider } from "react-router-dom";
import LoginPage from './routes/LoginPage';

import Root from './routes/Root';
import ErrorPage from './routes/ErrorPage';
import Bank from "./routes/Bank";
import GameBrowser from "./routes/GameBrowser";
import LeaderBoard from "./routes/LeaderBoard";
import TradePage from "./routes/TradePage";


const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
    children: [
      { index:true, element: <LoginPage/>},
      {
        path: "bank",
        element: <Bank />,
      },
      {
        path: "browseGames",
        element: <GameBrowser />,
      },
      {
        path: "leaderBoard",
        element: <LeaderBoard />,
      },
      {
        path: "playGame",
        element: <TradePage />,
      },
      {
        path: "loginRegister",
        element: <LoginPage />,
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
