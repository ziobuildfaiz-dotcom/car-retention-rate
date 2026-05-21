import ReactECharts from "echarts-for-react";
import type { RankingItem } from "../../types";

interface Props {
  data: RankingItem[];
  title: string;
}

export default function RetentionBarChart({ data, title }: Props) {
  const option = {
    title: { text: title, left: "center", textStyle: { fontSize: 16 } },
    tooltip: {
      trigger: "axis",
      axisPointer: { type: "shadow" },
      formatter: (params: any) => {
        const d = params[0];
        const item = data[d.dataIndex];
        return `<b>${item.brand_name} ${item.series_name}</b><br/>
          车型: ${item.model_name}<br/>
          年份: ${item.model_year}年<br/>
          保值率: ${item.retention}%<br/>
          指导价: ${item.guide_price ? item.guide_price + "万" : "N/A"}`;
      },
    },
    grid: { left: 140, right: 60, top: 50, bottom: 40 },
    xAxis: {
      type: "value",
      name: "保值率 (%)",
      max: 100,
    },
    yAxis: {
      type: "category",
      data: data
        .map(
          (d) =>
            `${d.brand_name} ${d.series_name} ${d.model_year}款`
        )
        .reverse(),
      axisLabel: { fontSize: 12 },
    },
    series: [
      {
        type: "bar",
        data: data
          .map((d) => ({
            value: d.retention,
            itemStyle: {
              color: d.retention >= 75 ? "#52c41a" : d.retention >= 60 ? "#faad14" : "#ff4d4f",
              borderRadius: [0, 4, 4, 0],
            },
          }))
          .reverse(),
        label: {
          show: true,
          position: "right",
          formatter: "{c}%",
          fontSize: 12,
        },
      },
    ],
  };

  return <ReactECharts option={option} style={{ height: 450 }} />;
}
