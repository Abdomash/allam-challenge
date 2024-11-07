import { ChatLogContext } from '@/contexts/DataContext'
import { ChatEntry } from '@/lib/types'
import { PropsWithChildren, useEffect, useState } from 'react'

export function ChatLogProvider({ children }: PropsWithChildren) {
  const [chatLog, setChatLog] = useState<ChatEntry[]>([])

  // Initialize chat log from localStorage
  useEffect(() => {
    const storedChatLog = localStorage.getItem('chatLog')
    if (storedChatLog) {
      setChatLog(JSON.parse(storedChatLog))
    }
  }, [])

  // Save chat log to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('chatLog', JSON.stringify(chatLog))
  }, [chatLog])

  const addEntry = (entry: ChatEntry) => {
    setChatLog((prevChatLog) => [...prevChatLog, entry])
  }

  const updateLastEntry = (responseData: ChatEntry) => {
    setChatLog((prevChatLog) => {
      const newChatLog = [...prevChatLog]
      const lastEntry = { ...newChatLog.pop(), responseData } as ChatEntry
      return [...newChatLog, lastEntry]
    })
  }

  return (
    <ChatLogContext.Provider value={{ chatLog, addEntry, updateLastEntry }}>
      {children}
    </ChatLogContext.Provider>
  )
}
