import { ApiAnalyzeResponse } from '@/lib/types'
import AnalysisShatrView from './AnalysisShatrView'

export interface AnalyzeResponseProps {
  response: ApiAnalyzeResponse
}

export default function AnalyzeResponse({ response }: AnalyzeResponseProps) {
  return (
    <div className="grid grid-cols-2 gap-2 rounded-lg bg-primary p-4">
      {response.analyzed_shatrs.map((attempt) => (
        <AnalysisShatrView key={attempt.shatr_idx} attempt={attempt} />
      ))}
    </div>
  )
}
