import { useDataContext } from '@/hooks/useDataContext'
import UserMessage from './UserMessage'
import LLMResponse from './LLMResponse'
import { cn } from '@/lib/utils'

interface ChatViewProps {
  className?: string
}

export default function ChatView({ className }: ChatViewProps) {
  const dataContext = useDataContext()
  const { dataById } = dataContext.state

  return (
    <div
      className={cn('w-full md:max-w-3xl flex flex-col gap-4 p-4 ', className)}
    >
      <h2 className="text-center text-2xl font-bold">تاريخ المحادثة</h2>
      {Object.values(dataById).map(({ prompt, responses }) => (
        <div className="flex w-full flex-col gap-2">
          <UserMessage className="ml-auto" message={prompt} />
          <LLMResponse className="mr-auto" responses={responses} />
        </div>
      ))}
    </div>
  )
}
