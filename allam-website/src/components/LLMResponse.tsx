import { cn } from '@/lib/utils'
import { Skeleton } from './ui/skeleton'
import CyclingText from './CyclingText'
import { LoadingResponseTextAnimated } from '@/lib/constants'
import { ApiAnalyzeResponse, ApiGenerateResponse } from '@/lib/types'
import GenerateResponse from './GenerateResponse'
import AnalyzeResponse from './AnalyzeResponse'

// eslint-disable-next-line @typescript-eslint/no-unused-vars
function LoadingResponse({ className }: { className?: string }) {
  return (
    <div className={cn('flex flex-col gap-2 items-end', className)}>
      <CyclingText
        className="pl-4"
        strings={LoadingResponseTextAnimated}
        interval={3000}
      />
      <Skeleton className="grid h-28 w-72 grid-cols-2 gap-4 rounded-md bg-secondary p-4">
        {Array.from(Array(6).keys()).map(() => (
          <Skeleton className="h-4 w-full rounded-md bg-gray-400" />
        ))}
      </Skeleton>
    </div>
  )
}

interface LLMResponseProps {
  className?: string
  response: ApiGenerateResponse | ApiAnalyzeResponse
}

export default function LLMResponse({ response, className }: LLMResponseProps) {
  return (
    <div className={cn('text-sm text-muted-foreground', className)}>
      {response.type === 'analyze' && <AnalyzeResponse response={response} />}
      {response.type === 'generate' && <GenerateResponse response={response} />}
    </div>
  )
}
