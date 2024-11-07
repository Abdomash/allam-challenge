import { ChatLogContext } from '@/contexts/DataContext'
import { useContext } from 'react'

export function useChatLog() {
  const context = useContext(ChatLogContext)
  if (!context) {
    throw new Error('useChatLog must be used within a ChatLogProvider')
  }
  return context
}
