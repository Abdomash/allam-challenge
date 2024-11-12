import { cn } from '@/lib/utils'
import { Skeleton } from './ui/skeleton'
import CyclingText from './CyclingText'
import { LoadingResponseTextAnimated } from '@/lib/constants'
import {
  ApiAnalyzeRequest,
  ApiAnalyzeResponse,
  ApiGenerateRequest,
  ApiGenerateResponse,
} from '@/lib/types'
import GenerateResponse from './GenerateResponse'
import AnalyzeResponse from './AnalyzeResponse'
import { Loader2Icon } from 'lucide-react'
import { Badge } from './ui/badge'

function LoadingResponse({ className }: { className?: string }) {
  return (
    <div className={cn('flex flex-col gap-2 items-end', className)}>
      <div className="flex flex-row items-end gap-2">
        <CyclingText
          className="pl-4"
          strings={LoadingResponseTextAnimated}
          interval={3000}
        />
        <Loader2Icon className="size-6 animate-spin bg-transparent" />
      </div>
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
  response: ApiGenerateResponse | ApiAnalyzeResponse | undefined
  request: ApiAnalyzeRequest | ApiGenerateRequest
}

export default function LLMResponse({
  response,
  className,
  request,
}: LLMResponseProps) {
  if (!response) {
    return <LoadingResponse />
  }

  const poetRequested = request.type == 'generate' ? request.poet : 'المستخدم'
  const wazn_name =
    response.type == 'generate'
      ? response.attempts[0].wazn_name
      : response.analyzed_shatrs[0].wazn_name

  const ResponseComponent = ({
    response,
  }: {
    response: ApiAnalyzeResponse | ApiGenerateResponse
  }) => {
    return response.type === 'analyze' ? (
      <AnalyzeResponse response={response} />
    ) : (
      <GenerateResponse response={response} />
    )
  }

  return (
    <div className={cn('flex flex-col w-full gap-2 items-end', className)}>
      <div className="flex flex-row gap-3">
        <Badge
          variant="outline"
          className={
            response.type === 'analyze' ? 'bg-primary' : 'bg-secondary'
          }
        >
          {response.type === 'analyze' ? 'نمط المحلل' : 'نمط التوليد'}
        </Badge>
        <Badge className="bg-secondary">الشاعر: {poetRequested}</Badge>
        <Badge className="bg-secondary">بحر {wazn_name}</Badge>
      </div>
      <ResponseComponent response={response} />
    </div>
  )
}
