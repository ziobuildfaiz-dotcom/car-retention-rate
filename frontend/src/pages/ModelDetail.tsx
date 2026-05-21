import { Card, Descriptions, Spin, Typography, Tag, Space, Button } from "antd";
import { useParams, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import ReactECharts from "echarts-for-react";
import { fetchModelDetail } from "../api/retention";
import { useComparison } from "../hooks/useComparison";

const { Title } = Typography;

export default function ModelDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const addModel = useComparison((s) => s.addModel);
  const modelIds = useComparison((s) => s.modelIds);

  const { data: model, isLoading } = useQuery({
    queryKey: ["model", id],
    queryFn: () => fetchModelDetail(Number(id)),
    enabled: !!id,
  });

  if (isLoading) {
    return <div style={{ textAlign: "center", padding: 80 }}><Spin size="large" /></div>;
  }

  if (!model) {
    return <div style={{ textAlign: "center", padding: 80 }}>车型未找到</div>;
  }

  const latestRate = model.retention_rates?.[0];
  const years = ["1年", "2年", "3年", "4年", "5年"];
  const values = latestRate
    ? [
        latestRate.retention_1yr,
        latestRate.retention_2yr,
        latestRate.retention_3yr,
        latestRate.retention_4yr,
        latestRate.retention_5yr,
      ]
    : [];

  const curveOption = {
    title: { text: "保值率衰减曲线", left: "center" },
    tooltip: { trigger: "axis" },
    xAxis: { type: "category", data: years },
    yAxis: { type: "value", name: "保值率 (%)", min: 0, max: 100 },
    series: [
      {
        type: "line",
        data: values,
        smooth: true,
        lineStyle: { width: 3, color: "#1677ff" },
        itemStyle: { color: "#1677ff" },
        areaStyle: {
          color: {
            type: "linear",
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: "rgba(22, 119, 255, 0.3)" },
              { offset: 1, color: "rgba(22, 119, 255, 0.05)" },
            ],
          },
        },
        markLine: {
          silent: true,
          data: [{ yAxis: 60, lineStyle: { color: "#faad14", type: "dashed" }, label: { formatter: "60% 基准线" } }],
        },
      },
    ],
  };

  return (
    <div>
      <div className="page-header">
        <Title level={2}>
          {model.brand_name} {model.series_name} {model.specific_model}
        </Title>
      </div>

      <Space style={{ marginBottom: 16 }}>
        <Button onClick={() => navigate(-1)}>返回</Button>
        <Button type="primary" onClick={() => addModel(model.id)}>
          {modelIds.includes(model.id) ? "已加入对比" : "加入对比"} ({modelIds.length}/5)
        </Button>
        <Button onClick={() => navigate("/compare")}>前往对比页</Button>
      </Space>

      <Card style={{ marginBottom: 16 }}>
        <Descriptions bordered column={{ xs: 1, sm: 2, md: 3 }}>
          <Descriptions.Item label="品牌">{model.brand_name}</Descriptions.Item>
          <Descriptions.Item label="车系">{model.series_name}</Descriptions.Item>
          <Descriptions.Item label="车型年份">{model.model_year}年</Descriptions.Item>
          <Descriptions.Item label="指导价">
            {model.guide_price ? `${model.guide_price} 万元` : "N/A"}
          </Descriptions.Item>
          <Descriptions.Item label="排量">{model.displacement || "N/A"}</Descriptions.Item>
          <Descriptions.Item label="燃料类型">
            <Tag color={model.fuel_type === "纯电" ? "green" : model.fuel_type === "混动" || model.fuel_type === "插混" ? "blue" : "default"}>
              {model.fuel_type || "N/A"}
            </Tag>
          </Descriptions.Item>
          <Descriptions.Item label="变速箱">{model.transmission || "N/A"}</Descriptions.Item>
          {latestRate && (
            <>
              <Descriptions.Item label="数据来源">{latestRate.source}</Descriptions.Item>
              <Descriptions.Item label="样本量">{latestRate.sample_count}</Descriptions.Item>
            </>
          )}
        </Descriptions>
      </Card>

      <Card>
        <ReactECharts option={curveOption} style={{ height: 400 }} />
      </Card>

      {latestRate && (
        <Card title="保值率明细" style={{ marginTop: 16 }}>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))", gap: 16 }}>
            {[
              { label: "1年", value: latestRate.retention_1yr },
              { label: "2年", value: latestRate.retention_2yr },
              { label: "3年", value: latestRate.retention_3yr },
              { label: "4年", value: latestRate.retention_4yr },
              { label: "5年", value: latestRate.retention_5yr },
            ].map(({ label, value }) => (
              <Card key={label} size="small" style={{ textAlign: "center" }}>
                <div style={{ fontSize: 12, color: "#666" }}>{label}保值率</div>
                <div style={{ fontSize: 28, fontWeight: 700, color: value && value >= 70 ? "#52c41a" : value && value >= 55 ? "#faad14" : "#ff4d4f" }}>
                  {value != null ? `${value}%` : "N/A"}
                </div>
              </Card>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}
