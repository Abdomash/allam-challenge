import { useDataContext } from '@/hooks/useDataContext'
import UserMessage from './UserMessage'
import LLMResponse from './LLMResponse'
import { cn } from '@/lib/utils'

interface ChatViewProps {
  className?: string
}

export default function ChatView({ className }: ChatViewProps) {
  // TODO: Change datacontext
  const dataContext = useDataContext()
  const { dataById } = dataContext.state
  const entries = Object.values(dataById) || []

  return (
    <div
      className={cn('w-full md:max-w-3xl flex flex-col gap-4 p-4 ', className)}
    >
      <h2 className="text-center text-2xl font-bold">تاريخ المحادثة</h2>
      {entries.map((entry) => (
        <div className="flex w-full flex-col gap-2">
          <UserMessage request={entry.request} />
          <LLMResponse response={entry.response} />
        </div>
      ))}
    </div>
  )
}
