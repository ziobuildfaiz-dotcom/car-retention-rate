import ReactECharts from "echarts-for-react";
import type { BrandRankingItem } from "../../types";

interface Props {
  data: BrandRankingItem[];
  title: string;
}

export default function RetentionTrendLine({ data, title }: Props) {
  const option = {
    title: { text: title, left: "center", textStyle: { fontSize: 16 } },
    tooltip: {
      trigger: "axis",
      formatter: (params: any) => {
        const d = params[0];
        const item = data[d.dataIndex];
        return `<b>${item.brand_name}</b><br/>
          平均保值率: ${item.avg_retention}%<br/>
          车型数量: ${item.model_count}`;
      },
    },
    grid: { left: 100, right: 60, top: 50, bottom: 50 },
    xAxis: {
      type: "category",
      data: data.map((d) => d.brand_name),
      axisLabel: { fontSize: 12, rotate: 30 },
    },
    yAxis: {
      type: "value",
      name: "保值率 (%)",
      min: (v: { min: number }) => Math.floor(v.min / 5) * 5,
      max: (v: { max: number }) => Math.ceil(v.max / 5) * 5,
    },
    series: [
      {
        type: "line",
        data: data.map((d) => d.avg_retention),
        smooth: true,
        lineStyle: { width: 3, color: "#1677ff" },
        itemStyle: { color: "#1677ff" },
        areaStyle: {
          color: {
            type: "linear",
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: "rgba(22, 119, 255, 0.3)" },
              { offset: 1, color: "rgba(22, 119, 255, 0.05)" },
            ],
          },
        },
        label: {
          show: true,
          position: "top",
          formatter: "{c}%",
          fontSize: 12,
        },
      },
      {
        type: "bar",
        data: data.map((d) => d.model_count),
        yAxisIndex: 1,
        barWidth: 20,
        itemStyle: {
          color: "rgba(250, 173, 20, 0.35)",
          borderRadius: [4, 4, 0, 0],
        },
        label: {
          show: true,
          position: "top",
          formatter: "{c}款",
          fontSize: 10,
        },
      },
    ],
  };

  return <ReactECharts option={option} style={{ height: 400 }} />;
}
