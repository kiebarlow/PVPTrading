import React, { useEffect, useState, useRef } from 'react';
import Plot from "react-plotly.js";

const TradeView = ({ data }) => {
  const chartData = [
    {
      x: data.map((d) => new Date(d.time * 1000)), // Convert UNIX timestamp to Date
      close: data.map((d) => d.close),
      high: data.map((d) => d.high),
      low: data.map((d) => d.low),
      open: data.map((d) => d.open),
      type: "candlestick",
      name: "BTC/USDT",
      increasing: { line: { color: "green" } },
      decreasing: { line: { color: "red" } },
    },
  ];

  const layout = {
    title: "BTC/USDT Candlestick Chart",
    xaxis: { rangeslider: { visible: false } },
    yaxis: { title: "Price (USDT)" },
    plot_bgcolor: "#0D0D0D",
    paper_bgcolor: "0D0D0D",
  };

  return <Plot data={chartData} layout={layout} style={{ width: '100%', height: '100%' }}/>;
};

export default TradeView 