import { createContext, useContext } from "react";

export interface SidebarContextValue {
  collapsed: boolean;
  toggleSidebar: () => void;
}

export const SidebarContext = createContext<SidebarContextValue | null>(null);

export function useSidebar(): SidebarContextValue {
  const context = useContext(SidebarContext);

  if (!context) {
    throw new Error("useSidebar must be used within SidebarProvider");
  }

  return context;
}
