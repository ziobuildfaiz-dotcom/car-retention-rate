import { Row, Col, Card, Spin, Empty, Typography } from "antd";
import { useQuery } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { fetchRankings, fetchBrandRankings, fetchBrands } from "../api/retention";
import { useFilters } from "../hooks/useFilters";
import { useComparison } from "../hooks/useComparison";
import FilterBar from "../components/filters/FilterBar";
import RetentionBarChart from "../components/charts/RetentionBarChart";
import RetentionTrendLine from "../components/charts/RetentionTrendLine";
import BrandRadarChart from "../components/charts/BrandRadarChart";

const { Title, Text } = Typography;

export default function Dashboard() {
  const { filters, setFilter } = useFilters();
  const addModel = useComparison((s) => s.addModel);
  const navigate = useNavigate();

  const { data: rankings, isLoading: rankingsLoading } = useQuery({
    queryKey: ["rankings", filters],
    queryFn: () =>
      fetchRankings({
        retention_period: filters.retention_period,
        vehicle_type: filters.vehicle_type || undefined,
        model_year: filters.model_year || undefined,
        brand_id: filters.brand_id || undefined,
        top_n: 20,
      }),
  });

  const { data: brandRankings, isLoading: brandsLoading } = useQuery({
    queryKey: ["brandRankings", filters.retention_period],
    queryFn: () =>
      fetchBrandRankings({
        retention_period: filters.retention_period,
        top_n: 10,
      }),
  });

  const topBrands = (brandRankings || []).slice(0, 5);
  const radarData = topBrands.map((b) => ({
    name: b.brand_name,
    guide_price: null as number | null,
    values: [b.avg_retention, b.avg_retention - 2, b.avg_retention - 8, 60, b.model_count * 2],
  }));

  return (
    <div>
      <div className="page-header">
        <Title level={2}>汽车保值率仪表盘</Title>
        <Text type="secondary">
          覆盖近 20 年主流车型保值率数据，支持按品牌、车型、年份筛选
        </Text>
      </div>

      <FilterBar filters={filters} onChange={setFilter} />

      {rankingsLoading || brandsLoading ? (
        <div style={{ textAlign: "center", padding: 80 }}>
          <Spin size="large" />
        </div>
      ) : (
        <Row gutter={[16, 16]}>
          <Col xs={24} lg={12}>
            <Card>
              {rankings && rankings.length > 0 ? (
                <RetentionBarChart
                  data={rankings.slice(0, 15)}
                  title={`${filters.retention_period.replace("yr", "年")}保值率排行`}
                />
              ) : (
                <Empty description="暂无数据" />
              )}
            </Card>
          </Col>

          <Col xs={24} lg={12}>
            <Card>
              {brandRankings && brandRankings.length > 0 ? (
                <RetentionTrendLine
                  data={brandRankings}
                  title="品牌保值率对比"
                />
              ) : (
                <Empty description="暂无数据" />
              )}
            </Card>
          </Col>

          <Col xs={24} lg={12}>
            <Card>
              {radarData.length >= 3 ? (
                <BrandRadarChart
                  data={radarData}
                  dimensions={["平均保值率", "1年保值率", "5年保值率", "市场热度", "样本覆盖"]}
                  title="Top5 品牌雷达对比"
                />
              ) : (
                <Empty description="需要至少 3 个品牌数据才能显示雷达图" />
              )}
            </Card>
          </Col>

          <Col xs={24} lg={12}>
            <Card title="快速操作">
              <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                {(rankings || []).slice(0, 5).map((item) => (
                  <div
                    key={item.model_id}
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      padding: "8px 12px",
                      background: "#fafafa",
                      borderRadius: 6,
                      cursor: "pointer",
                    }}
                    onClick={() => navigate(`/models/${item.model_id}`)}
                  >
                    <div>
                      <Text strong>
                        #{item.rank} {item.brand_name} {item.series_name}
                      </Text>
                      <br />
                      <Text type="secondary" style={{ fontSize: 12 }}>
                        {item.model_name} ({item.model_year}年)
                      </Text>
                    </div>
                    <div style={{ textAlign: "right" }}>
                      <Text
                        strong
                        style={{
                          fontSize: 18,
                          color:
                            item.retention >= 75
                              ? "#52c41a"
                              : item.retention >= 60
                                ? "#faad14"
                                : "#ff4d4f",
                        }}
                      >
                        {item.retention}%
                      </Text>
                      <br />
                      <Text
                        type="secondary"
                        style={{ fontSize: 12, cursor: "pointer" }}
                        onClick={(e) => {
                          e.stopPropagation();
                          addModel(item.model_id);
                        }}
                      >
                        + 加入对比
                      </Text>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </Col>
        </Row>
      )}
    </div>
  );
}
