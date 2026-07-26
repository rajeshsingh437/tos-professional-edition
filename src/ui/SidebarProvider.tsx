import { useEffect, useMemo, useState, type ReactNode } from "react";

import { SidebarContext, type SidebarContextValue } from "./SidebarContext";

interface SidebarProviderProps {
  children: ReactNode;
}

const STORAGE_KEY = "tos.sidebar.collapsed";

export default function SidebarProvider({ children }: SidebarProviderProps) {
  const [collapsed, setCollapsed] = useState(false);

  useEffect(() => {
    console.log("SidebarProvider mounted");

    const stored = localStorage.getItem(STORAGE_KEY);

    if (stored !== null) {
      setCollapsed(stored === "true");
    }
  }, []);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, String(collapsed));
  }, [collapsed]);

  const value = useMemo<SidebarContextValue>(
    () => ({
      collapsed,
      toggleSidebar: () => {
        setCollapsed((previous) => !previous);
      },
    }),
    [collapsed],
  );

  return (
    <SidebarContext.Provider value={value}>{children}</SidebarContext.Provider>
  );
}
