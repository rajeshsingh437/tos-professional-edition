import "./App.css";

import MainLayout from "./components/layout/MainLayout";
import Sidebar from "./components/layout/Sidebar";

function App() {
  return (
    <MainLayout>
      <Sidebar />

      <main className="content">
        <h1>Trading Operating System</h1>
        <p>Dashboard Loading...</p>
      </main>
    </MainLayout>
  );
}

export default App;