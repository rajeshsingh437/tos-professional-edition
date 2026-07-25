import { createBrowserRouter } from "react-router-dom";

import Dashboard from "../pages/Dashboard/Dashboard";
import TradeBookPage from "../pages/Journal/TradeBookPage";

import AppLayout from "./AppLayout";

const Placeholder = ({ title }: { title: string }) => (
  <div
    style={{
      padding: "24px",
      color: "#ffffff",
    }}
  >
    <h1>{title}</h1>
    <p>This module is under development.</p>
  </div>
);

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    children: [
      {
        index: true,
        element: <Dashboard />,
      },
      {
        path: "trading",
        element: <Placeholder title="Trading" />,
      },
      {
        path: "journal",
        element: <TradeBookPage />,
      },
      {
        path: "analytics",
        element: <Placeholder title="Analytics" />,
      },
      {
        path: "risk",
        element: <Placeholder title="Risk Manager" />,
      },
      {
        path: "ai",
        element: <Placeholder title="AI Assistant" />,
      },
      {
        path: "settings",
        element: <Placeholder title="Settings" />,
      },
    ],
  },
]);
