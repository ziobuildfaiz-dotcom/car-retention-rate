import ReactECharts from "echarts-for-react";

interface RadarEntry {
  name: string;
  values: number[];
}

interface Props {
  data: RadarEntry[];
  dimensions: string[];
  title: string;
}

export default function BrandRadarChart({ data, dimensions, title }: Props) {
  const option = {
    title: { text: title, left: "center", textStyle: { fontSize: 16 } },
    tooltip: { trigger: "item" },
    legend: {
      data: data.map((d) => d.name),
      bottom: 0,
    },
    radar: {
      indicator: dimensions.map((dim) => ({ name: dim, max: 100 })),
      center: ["50%", "50%"],
      radius: "65%",
    },
    series: [
      {
        type: "radar",
        data: data.map((d) => ({
          name: d.name,
          value: d.values,
        })),
        areaStyle: { opacity: 0.15 },
      },
    ],
  };

  return <ReactECharts option={option} style={{ height: 400 }} />;
}
