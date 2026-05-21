import { create } from "zustand";

interface ComparisonStore {
  modelIds: number[];
  addModel: (id: number) => void;
  removeModel: (id: number) => void;
  clear: () => void;
}

export const useComparison = create<ComparisonStore>((set) => ({
  modelIds: [],
  addModel: (id) =>
    set((s) => ({
      modelIds: s.modelIds.includes(id) ? s.modelIds : [...s.modelIds, id].slice(-5),
    })),
  removeModel: (id) =>
    set((s) => ({ modelIds: s.modelIds.filter((mid) => mid !== id) })),
  clear: () => set({ modelIds: [] }),
}));
