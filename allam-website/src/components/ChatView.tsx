import UserMessage from './UserMessage'
import LLMResponse from './LLMResponse'
import { cn } from '@/lib/utils'
import { useChatLog } from '@/hooks/useChatLog'

interface ChatViewProps {
  className?: string
}

export default function ChatView({ className }: ChatViewProps) {
  // use useChatLog hook to get the chat log
  const { chatLog } = useChatLog()

  return (
    <div
      className={cn('w-full md:max-w-3xl flex flex-col gap-4 p-4 ', className)}
    >
      <h2 className="text-center text-2xl font-bold">تاريخ المحادثة</h2>
      {chatLog.map((entry) => (
        <div className="flex w-full flex-col gap-2">
          <UserMessage request={entry.request} />
          <LLMResponse response={entry.response} />
        </div>
      ))}
    </div>
  )
}
