import { Select, Space, Tag } from "antd";
import { useQuery } from "@tanstack/react-query";
import { fetchBrands, fetchFilterMeta } from "../../api/retention";
import type { FilterState } from "../../hooks/useFilters";

interface Props {
  filters: FilterState;
  onChange: (key: keyof FilterState, value: string | number | null) => void;
}

const RETENTION_OPTIONS = [
  { label: "1年保值率", value: "1yr" },
  { label: "3年保值率", value: "3yr" },
  { label: "5年保值率", value: "5yr" },
];

export default function FilterBar({ filters, onChange }: Props) {
  const { data: meta } = useQuery({
    queryKey: ["filterMeta"],
    queryFn: fetchFilterMeta,
  });

  const { data: brands } = useQuery({
    queryKey: ["brands", ""],
    queryFn: () => fetchBrands({ page_size: 100 }),
  });

  return (
    <div className="filter-bar">
      <Space wrap size="middle">
        <Select
          placeholder="选择品牌"
          style={{ width: 180 }}
          allowClear
          showSearch
          value={filters.brand_id}
          onChange={(v) => onChange("brand_id", v)}
          options={(brands?.items || []).map((b) => ({
            label: b.name,
            value: b.id,
          }))}
          filterOption={(input, option) =>
            (option?.label as string)?.includes(input)
          }
        />

        <Select
          placeholder="车辆类型"
          style={{ width: 120 }}
          allowClear
          value={filters.vehicle_type}
          onChange={(v) => onChange("vehicle_type", v)}
          options={(meta?.vehicle_types || []).map((t) => ({
            label: t,
            value: t,
          }))}
        />

        <Select
          placeholder="保值年限"
          style={{ width: 140 }}
          value={filters.retention_period}
          onChange={(v) => onChange("retention_period", v)}
          options={RETENTION_OPTIONS}
        />

        <Select
          placeholder="车型年份"
          style={{ width: 120 }}
          allowClear
          value={filters.model_year}
          onChange={(v) => onChange("model_year", v)}
          options={
            meta
              ? Array.from(
                  { length: meta.year_range[1] - meta.year_range[0] + 1 },
                  (_, i) => ({
                    label: String(meta.year_range[0] + i),
                    value: meta.year_range[0] + i,
                  })
                ).reverse()
              : []
          }
        />
      </Space>
    </div>
  );
}
