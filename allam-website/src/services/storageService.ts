import { ApiResponse, Progress } from '../lib/types'

const STORAGE_KEY = 'progressionData'

export function saveData(response: ApiResponse): void {
  const { request_id, progression } = response

  // Load existing data from local storage
  const existingData = loadData()

  // Update the data with the new response
  const updatedData = {
    ...existingData,
    [request_id]: progression,
  }

  // Save back to local storage
  localStorage.setItem(STORAGE_KEY, JSON.stringify(updatedData))
}

export function loadData(): Record<string, Progress> {
  const data = localStorage.getItem(STORAGE_KEY)
  return data ? JSON.parse(data) : {}
}

export function clearData(): void {
  localStorage.removeItem(STORAGE_KEY)
}
