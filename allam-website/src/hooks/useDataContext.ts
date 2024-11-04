import { DataContext } from '@/contexts/DataContext'
import { useContext } from 'react'

export function useDataContext() {
  const data = useContext(DataContext)

  if (data === undefined) {
    throw new Error('useDataContext must be used within a DataProvider')
  }

  return data
}
