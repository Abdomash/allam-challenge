import { ApiResponse } from '../lib/types'

export async function fetchDataFromApi(endpoint: string): Promise<ApiResponse> {
  const response = await fetch(endpoint)
  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`)
  }
  const data: ApiResponse = await response.json()
  return data
}
