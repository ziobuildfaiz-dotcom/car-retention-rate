import { useSearchParams } from "react-router-dom";
import { useCallback, useMemo } from "react";

export interface FilterState {
  brand_id: number | null;
  vehicle_type: string | null;
  model_year: number | null;
  retention_period: string;
}

export function useFilters() {
  const [searchParams, setSearchParams] = useSearchParams();

  const filters: FilterState = useMemo(
    () => ({
      brand_id: searchParams.get("brand_id") ? Number(searchParams.get("brand_id")) : null,
      vehicle_type: searchParams.get("vehicle_type") || null,
      model_year: searchParams.get("model_year") ? Number(searchParams.get("model_year")) : null,
      retention_period: searchParams.get("retention_period") || "3yr",
    }),
    [searchParams]
  );

  const setFilter = useCallback(
    (key: keyof FilterState, value: string | number | null) => {
      setSearchParams((prev) => {
        const next = new URLSearchParams(prev);
        if (value === null || value === "") {
          next.delete(key);
        } else {
          next.set(key, String(value));
        }
        return next;
      });
    },
    [setSearchParams]
  );

  const clearFilters = useCallback(() => {
    setSearchParams({});
  }, [setSearchParams]);

  return { filters, setFilter, clearFilters };
}
