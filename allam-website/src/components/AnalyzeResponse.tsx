import { ApiAnalyzeResponse } from '@/lib/types'

export interface AnalyzeResponseProps {
  response: ApiAnalyzeResponse
}

export default function AnalyzeResponse({ response }: AnalyzeResponseProps) {
  return (
    <div className="flex flex-col items-end gap-2">
      <p>{response.feedback}</p>
      <p>{response.wazn_comb}</p>
      <p>{response.wazn_mismatch}</p>
    </div>
  )
}
