import { useQuery } from '@tanstack/react-query'
import { fetchDataFromApi } from '../services/apiService'
import { ApiResponse } from '../lib/types'
import { saveData } from '../services/storageService'

interface UseApiDataOptions {
  endpoint: string
}

export function useApiData({ endpoint }: UseApiDataOptions) {
  return useQuery<ApiResponse, Error>(
    ['apiData', endpoint],
    async () => {
      const data = await fetchDataFromApi(endpoint)
      saveData(data) // Save data to local storage
      return data
    },
    {
      staleTime: 0,
    },
  )
}
