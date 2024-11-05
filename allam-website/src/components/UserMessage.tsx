import { cn } from '@/lib/utils'

export interface UserMessageProps {
  className?: string
  message: string
}

export default function UserMessage({ className, message }: UserMessageProps) {
  return (
    <p
      className={cn(
        'text-sm bg-primary p-2 rounded-md justify-start',
        className,
      )}
    >
      {message}
    </p>
  )
}
