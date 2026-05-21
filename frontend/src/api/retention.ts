import client from "./client";
import type {
  Brand,
  BrandRankingItem,
  CarModel,
  FilterMeta,
  ModelDetail,
  RadarData,
  RankingItem,
  Series,
} from "../types";

export async function fetchRankings(params: {
  retention_period?: string;
  vehicle_type?: string;
  model_year?: number;
  brand_id?: number;
  top_n?: number;
}): Promise<RankingItem[]> {
  const { data } = await client.get("/rankings", { params });
  return data;
}

export async function fetchBrandRankings(params: {
  retention_period?: string;
  top_n?: number;
}): Promise<BrandRankingItem[]> {
  const { data } = await client.get("/rankings/brands", { params });
  return data;
}

export async function fetchFilterMeta(): Promise<FilterMeta> {
  const { data } = await client.get("/meta/filters");
  return data;
}

export async function fetchBrands(params: {
  country?: string;
  search?: string;
  page?: number;
  page_size?: number;
}): Promise<{ items: Brand[]; total: number }> {
  const { data } = await client.get("/brands", { params });
  return data;
}

export async function fetchBrandDetail(id: number): Promise<Brand & { series_list: Series[] }> {
  const { data } = await client.get(`/brands/${id}`);
  return data;
}

export async function fetchModels(params: {
  series_id?: number;
  model_year?: number;
  fuel_type?: string;
  page?: number;
  page_size?: number;
}): Promise<{ items: CarModel[]; total: number }> {
  const { data } = await client.get("/models", { params });
  return data;
}

export async function fetchModelDetail(id: number): Promise<ModelDetail> {
  const { data } = await client.get(`/models/${id}`);
  return data;
}

export async function compareModels(modelIds: number[]): Promise<{
  models: CarModel[];
  radar_data: RadarData;
}> {
  const { data } = await client.post("/comparison", { model_ids: modelIds });
  return data;
}

export async function compareBrands(params: {
  brand_ids: number[];
  year_start?: number;
  year_end?: number;
}): Promise<{
  brands: { name: string; yearly: { year: number; avg_3yr: number }[] }[];
}> {
  const { data } = await client.post("/comparison/brands", params);
  return data;
}
