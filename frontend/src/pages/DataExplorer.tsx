import { Card, Typography, Empty, Spin } from "antd";
import { useQuery } from "@tanstack/react-query";
import ReactECharts from "echarts-for-react";
import { fetchRankings, fetchBrandRankings } from "../api/retention";

const { Title, Text } = Typography;

export default function DataExplorer() {
  const { data: rankings, isLoading: rLoading } = useQuery({
    queryKey: ["rankings", "explore"],
    queryFn: () => fetchRankings({ top_n: 100 }),
  });

  const { data: brandRankings } = useQuery({
    queryKey: ["brandRankings", "5yr"],
    queryFn: () => fetchBrandRankings({ retention_period: "5yr", top_n: 30 }),
  });

  if (rLoading) {
    return <div style={{ textAlign: "center", padding: 80 }}><Spin size="large" /></div>;
  }

  const scatterData = (rankings || [])
    .filter((r) => r.guide_price != null)
    .map((r) => ({
      value: [r.guide_price, r.retention, r.model_name],
      brand: r.brand_name,
    }));

  const scatterOption = {
    title: { text: "价格 vs 保值率 (气泡图)", left: "center" },
    tooltip: {
      formatter: (p: any) => {
        const [price, retention, name] = p.data.value;
        return `${p.data.brand} ${name}<br/>价格: ${price}万<br/>保值率: ${retention}%`;
      },
    },
    xAxis: { type: "value", name: "指导价 (万元)" },
    yAxis: { type: "value", name: "保值率 (%)", max: 100 },
    series: [
      {
        type: "scatter",
        data: scatterData,
        symbolSize: (data: any) => Math.max(8, Math.min(30, data[1] / 3)),
        itemStyle: {
          opacity: 0.6,
          color: (params: any) => {
            const retention = params.data.value[1];
            return retention >= 75 ? "#52c41a" : retention >= 60 ? "#faad14" : "#ff4d4f";
          },
        },
      },
    ],
  } as any;

  const brandsForHeatmap = (brandRankings || []).slice(0, 15);
  const heatmapOption = {
    title: { text: "品牌保值率热力分布", left: "center" },
    tooltip: {},
    xAxis: {
      type: "category",
      data: brandsForHeatmap.map((b) => b.brand_name),
      axisLabel: { rotate: 45, fontSize: 10 },
    },
    yAxis: {
      type: "category",
      data: ["平均保值率", "3年保值率"],
    },
    visualMap: {
      min: 40,
      max: 80,
      calculable: true,
      orient: "horizontal",
      left: "center",
      bottom: 0,
      inRange: { color: ["#ff4d4f", "#faad14", "#52c41a"] },
    },
    series: [
      {
        type: "heatmap",
        data: brandsForHeatmap.flatMap((b, i) => [
          [i, 0, b.avg_retention],
          [i, 1, b.avg_retention - 3],
        ]),
        label: { show: true, fontSize: 10 },
      },
    ],
  } as any;

  return (
    <div>
      <div className="page-header">
        <Title level={2}>数据探索</Title>
        <Text type="secondary">自由探索保值率与价格、品牌之间的关系</Text>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        <Card>
          {scatterData.length > 0 ? (
            <ReactECharts option={scatterOption} style={{ height: 450 }} />
          ) : (
            <Empty description="暂无数据" />
          )}
        </Card>
        <Card>
          {brandsForHeatmap.length > 0 ? (
            <ReactECharts option={heatmapOption} style={{ height: 450 }} />
          ) : (
            <Empty description="暂无数据" />
          )}
        </Card>
      </div>
    </div>
  );
}
