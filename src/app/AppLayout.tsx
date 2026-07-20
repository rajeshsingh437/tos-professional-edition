import { Outlet } from "react-router-dom";

import Header from "../components/layout/Header";
import Sidebar from "../components/layout/Sidebar";

const AppLayout = () => {
  return (
    <div className="app-layout">
      <Sidebar />

      <main className="content">
        <Header />

        <div className="page-content">
          <Outlet />
        </div>
      </main>
    </div>
  );
};

export default AppLayout;
