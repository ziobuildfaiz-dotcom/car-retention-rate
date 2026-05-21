export interface Brand {
  id: number;
  name: string;
  name_en: string | null;
  country: string | null;
  logo_url: string | null;
}

export interface Series {
  id: number;
  brand_id: number;
  name: string;
  vehicle_type: string | null;
}

export interface CarModel {
  id: number;
  series_id: number;
  model_year: number;
  specific_model: string;
  guide_price: number | null;
  displacement: string | null;
  fuel_type: string | null;
  transmission: string | null;
  brand_name?: string | null;
  series_name?: string | null;
}

export interface RetentionRate {
  id: number;
  model_id: number;
  source: string;
  scrape_date: string;
  retention_1yr: number | null;
  retention_2yr: number | null;
  retention_3yr: number | null;
  retention_4yr: number | null;
  retention_5yr: number | null;
  avg_listed_price: number | null;
  sample_count: number | null;
}

export interface RankingItem {
  rank: number;
  model_id: number;
  model_name: string;
  series_name: string;
  brand_name: string;
  model_year: number;
  guide_price: number | null;
  retention: number;
}

export interface BrandRankingItem {
  rank: number;
  brand_id: number;
  brand_name: string;
  avg_retention: number;
  model_count: number;
}

export interface FilterMeta {
  vehicle_types: string[];
  fuel_types: string[];
  countries: string[];
  year_range: [number, number];
  price_range: [number, number];
}

export interface RadarEntry {
  name: string;
  guide_price: number | null;
  values: number[];
}

export interface RadarData {
  models: RadarEntry[];
  dimensions: string[];
}

export interface ModelDetail extends CarModel {
  retention_rates: RetentionRate[];
}
