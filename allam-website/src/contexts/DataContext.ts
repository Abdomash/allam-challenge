import {
  DataAction,
  DataState,
  StartRequestMessage,
} from '@/providers/DataProvider'
import { createContext } from 'react'

interface DataContextProps {
  state: DataState
  dispatch: React.Dispatch<DataAction>
  sendMessage: (message: StartRequestMessage) => void
}

export const DataContext = createContext<DataContextProps | undefined>(
  undefined,
)
