import { ApiGenerateResponse, Attempt } from '@/lib/types'
import ShatrView from './ShatrView'
import { useMemo } from 'react'

function groupAttemptsByShatrIdx(attempts: Attempt[]) {
  return attempts
    .sort((a, b) => a.iteration_number - b.iteration_number)
    .reduce((acc, attempt) => {
      const shatrIdx: number = attempt.shatr_idx

      if (!acc[shatrIdx]) acc[shatrIdx] = []
      acc[shatrIdx].push(attempt)
      return acc
    }, [] as Attempt[][])
}

export interface GenerateResponseProps {
  response: ApiGenerateResponse
}

export default function GenerateResponse({ response }: GenerateResponseProps) {
  const shatrAttempts = useMemo(
    () => groupAttemptsByShatrIdx(response.attempts),
    [response.attempts],
  )

  return (
    <div className="grid grid-cols-2 gap-2 rounded-lg bg-secondary p-4">
      {shatrAttempts.map((attempts, i) => (
        <ShatrView key={i} attempts={attempts} />
      ))}
    </div>
  )
}
