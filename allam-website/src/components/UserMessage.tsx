import { ApiAnalyzeRequest, ApiGenerateRequest } from '@/lib/types'
import { cn } from '@/lib/utils'

function RegularMessage({ text }: { text: string }) {
  return <p>{text}</p>
}

function BaitsMessage({ baits }: { baits: string[] }) {
  return (
    <div>
      {baits.map((bait, i) => (
        <>
          <p key={i}>{bait}</p>
          <br />
        </>
      ))}
    </div>
  )
}

export interface UserMessageProps {
  className?: string
  request: ApiAnalyzeRequest | ApiGenerateRequest
}

export default function UserMessage({ className, request }: UserMessageProps) {
  return (
    <div
      className={cn(
        'text-sm bg-primary p-2 rounded-md justify-start',
        className,
      )}
      {...(request.type === 'generate' && (
        <RegularMessage text={request.prompt} />
      ))}
      {...(request.type === 'analyze' && (
        <BaitsMessage baits={request.baits} />
      ))}
    ></div>
  )
}
