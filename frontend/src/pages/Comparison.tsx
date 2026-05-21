import { Card, Select, Button, Space, Typography, Empty, Spin } from "antd";
import { useQuery } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import ReactECharts from "echarts-for-react";
import { useComparison } from "../hooks/useComparison";
import { compareModels, fetchBrands, fetchModels } from "../api/retention";
import BrandRadarChart from "../components/charts/BrandRadarChart";
import { useState } from "react";

const { Title, Text } = Typography;

export default function Comparison() {
  const { modelIds, addModel, removeModel, clear } = useComparison();
  const navigate = useNavigate();
  const [searchResults, setSearchResults] = useState<any[]>([]);

  const { data: comparison, isLoading } = useQuery({
    queryKey: ["comparison", modelIds],
    queryFn: () => compareModels(modelIds),
    enabled: modelIds.length >= 2,
  });

  const { data: brands } = useQuery({
    queryKey: ["brands", "all"],
    queryFn: () => fetchBrands({ page_size: 100 }),
  });

  const handleSearch = async (value: string) => {
    if (!value || value.length < 1) {
      setSearchResults([]);
      return;
    }
    const result = await fetchModels({ page_size: 20 });
    setSearchResults(
      result.items.filter(
        (m) =>
          (m.series_name || "").includes(value) ||
          (m.brand_name || "").includes(value) ||
          (m.specific_model || "").includes(value)
      )
    );
  };

  const overlayOption = comparison?.models
    ? {
        title: { text: "3年保值率对比", left: "center" },
        tooltip: { trigger: "axis" },
        legend: {
          data: comparison.models.map(
            (m: any) => `${m.brand_name} ${m.series_name}`
          ),
          bottom: 0,
        },
        xAxis: {
          type: "category",
          data: ["1年", "2年", "3年", "4年", "5年"],
        },
        yAxis: { type: "value", name: "保值率 (%)", max: 100 },
        series: comparison.models.map((m: any) => ({
          name: `${m.brand_name} ${m.series_name}`,
          type: "line",
          smooth: true,
          data: [] as number[], // Will be filled if we fetch retention per model
        })),
      }
    : null;

  return (
    <div>
      <div className="page-header">
        <Title level={2}>车型对比</Title>
        <Text type="secondary">
          选择 2-5 个车型进行多维度对比分析 ({modelIds.length}/5)
        </Text>
      </div>

      <Card style={{ marginBottom: 16 }}>
        <Space direction="vertical" style={{ width: "100%" }} size="middle">
          <Select
            showSearch
            placeholder="搜索车型名称以添加到对比列表"
            style={{ width: "100%" }}
            filterOption={false}
            onSearch={handleSearch}
            onSelect={(value: number) => {
              addModel(value);
              setSearchResults([]);
            }}
            options={searchResults.map((m) => ({
              label: `${m.brand_name || ""} ${m.series_name || ""} ${m.specific_model} (${m.model_year}年)`,
              value: m.id,
            }))}
          />

          {modelIds.length === 0 && (
            <Empty description="请在上方搜索并选择车型加入对比" />
          )}

          <Space wrap>
            {modelIds.map((id) => (
              <Tag
                key={id}
                closable
                onClose={() => removeModel(id)}
                style={{ padding: "4px 8px", fontSize: 14 }}
              >
                车型 #{id}
              </Tag>
            ))}
          </Space>

          {modelIds.length > 0 && (
            <Space>
              <Button size="small" onClick={clear}>清空全部</Button>
              <Button size="small" type="primary" disabled={modelIds.length < 2}>
                开始对比 ({modelIds.length}/5)
              </Button>
            </Space>
          )}
        </Space>
      </Card>

      {isLoading ? (
        <div style={{ textAlign: "center", padding: 80 }}><Spin size="large" /></div>
      ) : comparison?.radar_data?.models?.length >= 2 ? (
        <>
          <Card style={{ marginBottom: 16 }}>
            <BrandRadarChart
              data={comparison.radar_data.models}
              dimensions={comparison.radar_data.dimensions}
              title="多维度对比雷达图"
            />
          </Card>

          <Card title="车型信息对比">
            <div style={{ display: "grid", gridTemplateColumns: `repeat(${comparison.models.length}, 1fr)`, gap: 16 }}>
              {comparison.models.map((m: any) => (
                <Card
                  key={m.id}
                  size="small"
                  hoverable
                  onClick={() => navigate(`/models/${m.id}`)}
                >
                  <Text strong>{m.brand_name}</Text>
                  <br />
                  <Text>{m.series_name}</Text>
                  <br />
                  <Text type="secondary" style={{ fontSize: 12 }}>
                    {m.specific_model}
                  </Text>
                  <br />
                  <Text type="secondary">{m.model_year}年 | {m.guide_price ? `${m.guide_price}万` : "N/A"}</Text>
                </Card>
              ))}
            </div>
          </Card>
        </>
      ) : modelIds.length >= 2 ? (
        <Empty description="无法获取对比数据" />
      ) : null}
    </div>
  );
}
