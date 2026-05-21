import { Card, Typography, Spin, Table, Tag } from "antd";
import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import ReactECharts from "echarts-for-react";
import { fetchBrandDetail, fetchRankings } from "../api/retention";

const { Title } = Typography;

export default function BrandAnalysis() {
  const { id } = useParams<{ id: string }>();

  const { data: brand, isLoading: brandLoading } = useQuery({
    queryKey: ["brand", id],
    queryFn: () => fetchBrandDetail(Number(id)),
    enabled: !!id,
  });

  const { data: rankings } = useQuery({
    queryKey: ["rankings", "brand", id],
    queryFn: () => fetchRankings({ brand_id: Number(id), top_n: 50 }),
    enabled: !!id,
  });

  if (brandLoading) {
    return <div style={{ textAlign: "center", padding: 80 }}><Spin size="large" /></div>;
  }

  if (!brand) {
    return <div style={{ textAlign: "center", padding: 80 }}>品牌未找到</div>;
  }

  const typeDistribution: Record<string, number> = {};
  brand.series_list.forEach((s) => {
    const t = s.vehicle_type || "其他";
    typeDistribution[t] = (typeDistribution[t] || 0) + 1;
  });

  const typeChart = {
    title: { text: "车型构成", left: "center" },
    tooltip: { trigger: "item" },
    series: [
      {
        type: "pie",
        radius: ["40%", "70%"],
        data: Object.entries(typeDistribution).map(([name, value]) => ({
          name,
          value,
        })),
        label: { formatter: "{b}: {c}个车系" },
      },
    ],
  };

  const yearColumns = [
    { title: "排名", dataIndex: "rank", key: "rank", width: 60 },
    { title: "车型", dataIndex: "model_name", key: "model_name", ellipsis: true },
    { title: "车系", dataIndex: "series_name", key: "series_name" },
    { title: "年份", dataIndex: "model_year", key: "model_year", width: 80 },
    {
      title: "保值率",
      dataIndex: "retention",
      key: "retention",
      width: 100,
      render: (v: number) => (
        <Tag color={v >= 75 ? "green" : v >= 60 ? "gold" : "red"}>{v}%</Tag>
      ),
    },
  ];

  return (
    <div>
      <div className="page-header">
        <Title level={2}>{brand.name} {brand.country && <Tag>{brand.country}</Tag>}</Title>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 16 }}>
        <Card title="品牌概览">
          <p>品牌: {brand.name} ({brand.name_en || "N/A"})</p>
          <p>国别: {brand.country || "N/A"}</p>
          <p>车系数: {brand.series_list.length}</p>
        </Card>
        <Card>
          <ReactECharts option={typeChart} style={{ height: 280 }} />
        </Card>
      </div>

      <Card title="车型保值率排行">
        <Table
          dataSource={rankings || []}
          columns={yearColumns}
          rowKey="model_id"
          pagination={{ pageSize: 10 }}
          size="small"
        />
      </Card>
    </div>
  );
}
