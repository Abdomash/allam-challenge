import { ApiGenerateResponse, Attempt } from '@/lib/types'
import ShatrView from './ShatrView'

export interface GenerateResponseProps {
  response: ApiGenerateResponse
}

export default function GenerateResponse({ response }: GenerateResponseProps) {
  // Reorder attempts by shatr_idx and make it an Attempt[][]
  const shatrAttempts: Attempt[][] = response.attempts.reduce(
    (acc, attempt) => {
      const shatrIdx: number = attempt.shatr_idx

      if (!acc[shatrIdx]) acc[shatrIdx] = []
      acc[shatrIdx].push(attempt)
      return acc
    },
    [] as Attempt[][],
  )

  return (
    <div className="grid grid-cols-2 gap-2">
      {shatrAttempts.map((attempts, i) => (
        <ShatrView key={i} attempts={attempts} />
      ))}
    </div>
  )
}
