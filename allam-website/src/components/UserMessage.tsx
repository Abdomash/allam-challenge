import { ApiAnalyzeRequest, ApiGenerateRequest } from '@/lib/types'
import { cn } from '@/lib/utils'

function RegularMessage({ text }: { text: string }) {
  return (
    <div>
      <p>{text}</p>
    </div>
  )
}

function ShatrsMessage({ shatrs }: { shatrs: string[] }) {
  return (
    <div>
      {shatrs.map((shatr, i) => (
        <>
          <p key={i}>{shatr}</p>
          <br />
        </>
      ))}
    </div>
  )
}

export interface UserMessageProps {
  className?: string
  request: ApiGenerateRequest | ApiAnalyzeRequest
}

export default function UserMessage({ className, request }: UserMessageProps) {
  console.log('request', request.type)
  return (
    <div
      className={cn(
        'text-sm bg-primary p-2 rounded-md justify-start',
        className,
      )}
    >
      {request.type === 'generate' && <RegularMessage text={request.prompt} />}
      {request.type === 'analyze' && <ShatrsMessage shatrs={request.shatrs} />}
    </div>
  )
}
