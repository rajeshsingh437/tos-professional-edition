import { AreaSeries, ColorType, createChart } from "lightweight-charts";
import { useEffect, useRef } from "react";

export default function EquityCurve() {
  const chartContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!chartContainerRef.current) return;

    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 340,

      layout: {
        background: {
          type: ColorType.Solid,
          color: "#1b2238",
        },
        textColor: "#94a3b8",
      },

      grid: {
        vertLines: {
          color: "#2b3655",
        },
        horzLines: {
          color: "#2b3655",
        },
      },

      rightPriceScale: {
        borderColor: "#2b3655",
      },

      timeScale: {
        borderColor: "#2b3655",
      },
    });

    const areaSeries = chart.addSeries(AreaSeries, {
      lineColor: "#3b82f6",

      topColor: "rgba(59,130,246,0.45)",

      bottomColor: "rgba(59,130,246,0.05)",
    });

    areaSeries.setData([
      { time: "2026-01-01", value: 1000000 },
      { time: "2026-01-15", value: 1012000 },
      { time: "2026-02-01", value: 1028000 },
      { time: "2026-02-15", value: 1019000 },
      { time: "2026-03-01", value: 1045000 },
      { time: "2026-03-15", value: 1063000 },
      { time: "2026-04-01", value: 1084000 },
      { time: "2026-04-15", value: 1101000 },
      { time: "2026-05-01", value: 1126000 },
      { time: "2026-05-15", value: 1142000 },
      { time: "2026-06-01", value: 1165000 },
      { time: "2026-06-15", value: 1186000 },
    ]);

    chart.timeScale().fitContent();

    const resize = () => {
      if (!chartContainerRef.current) return;

      chart.applyOptions({
        width: chartContainerRef.current.clientWidth,
      });
    };

    window.addEventListener("resize", resize);

    return () => {
      window.removeEventListener("resize", resize);
      chart.remove();
    };
  }, []);

  return (
    <div className="equity-card">
      <div className="equity-header">
        <div>
          <h3>Equity Curve</h3>
          <span>Portfolio Growth</span>
        </div>

        <div className="equity-change">+18.6%</div>
      </div>

      <div ref={chartContainerRef} className="equity-chart" />

      <div className="equity-footer">
        <div>
          <small>Starting Capital</small>
          <strong>₹10,00,000</strong>
        </div>

        <div>
          <small>Current Equity</small>
          <strong>₹11,86,000</strong>
        </div>

        <div>
          <small>Max Drawdown</small>
          <strong>-3.2%</strong>
        </div>
      </div>
    </div>
  );
}
