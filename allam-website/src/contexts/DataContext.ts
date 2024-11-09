// ChatLogContext.tsx
import { ChatEntry } from '@/lib/types'
import { createContext } from 'react'

interface ChatLogContextType {
  chatLog: ChatEntry[]
  addEntry: (entry: ChatEntry) => void
  updateLastEntry: (entry: ChatEntry) => void
}

export const ChatLogContext = createContext<ChatLogContextType | undefined>(
  undefined,
)
