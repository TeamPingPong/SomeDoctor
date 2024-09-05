// store/resultStore.ts
import { create } from 'zustand'

type ResultState = {
  result: any
  setResult: (result: any) => void
}

export const useResultStore = create<ResultState>((set) => ({
  result: null,
  setResult: (result) => set({ result }),
}))