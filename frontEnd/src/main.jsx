import React from "react";
import ReactDOM from "react-dom/client";

import './index.css'


import { createBrowserRouter, RouterProvider } from "react-router-dom";
import LoginPage from './routes/LoginPage';

import Root from './routes/Root';
import ErrorPage from './routes/ErrorPage';

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "loginPage",
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
