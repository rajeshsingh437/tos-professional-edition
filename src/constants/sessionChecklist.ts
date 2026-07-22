export interface ChecklistItem {
  id: number;
  title: string;
  completed: boolean;
  weight: number;
}

export const sessionChecklist: ChecklistItem[] = [
  {
    id: 1,
    title: "Trading Plan Prepared",
    completed: true,
    weight: 20,
  },
  {
    id: 2,
    title: "Daily Risk Defined",
    completed: true,
    weight: 20,
  },
  {
    id: 3,
    title: "Economic Calendar Checked",
    completed: true,
    weight: 15,
  },
  {
    id: 4,
    title: "Important News Reviewed",
    completed: true,
    weight: 15,
  },
  {
    id: 5,
    title: "Sleep ≥ 7 Hours",
    completed: true,
    weight: 10,
  },
  {
    id: 6,
    title: "Emotional State Calm",
    completed: false,
    weight: 20,
  },
];
