import UserMessage from './UserMessage'
import LLMResponse from './LLMResponse'
import { cn } from '@/lib/utils'
import { useChatLog } from '@/hooks/useChatLog'
import { useEffect, useRef } from 'react'

interface ChatViewProps {
  className?: string
}

export default function ChatView({ className }: ChatViewProps) {
  // use useChatLog hook to get the chat log
  const { chatLog } = useChatLog()
  const containerRef = useRef<HTMLDivElement | null>(null)
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight
    }
  }, [chatLog])

  return (
    <div
      ref={containerRef}
      className={cn(
        'w-full pb-4 md:max-w-3xl flex flex-col gap-2 scroll-smooth',
        className,
      )}
    >
      {chatLog.map((entry, i) => (
        <div key={i} className="mb-4 flex w-full flex-col gap-2">
          <UserMessage request={entry.request} />
          <LLMResponse response={entry.response} request={entry.request} />
        </div>
      ))}
    </div>
  )
}
