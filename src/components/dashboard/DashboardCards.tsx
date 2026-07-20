
export default function DashboardCards()
 {
  const cards = [
    {
      title: "Portfolio Value",
      value: "₹12,45,000",
    },
    {
      title: "Today's P/L",
      value: "+₹14,520",
    },
    {
      title: "Win Rate",
      value: "63.4%",
    },
    {
      title: "Average R:R",
      value: "2.15",
    },
  ];

  return (
    <div className="dashboard-cards">
      {cards.map((card) => (
        <div className="dashboard-card" key={card.title}>
          <div className="card-title">{card.title}</div>
          <div className="card-value">{card.value}</div>
        </div>
      ))}
    </div>
  );
}
