import { Attempt } from '@/lib/types'
import { Button } from './ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from './ui/dropdown-menu'

export interface ShatrViewProps {
  attempts: Attempt[]
}

export default function ShatrView({ attempts }: ShatrViewProps) {
  // sort attempts by iteration number
  attempts.sort((a, b) => a.iteration_number - b.iteration_number)

  return (
    <div className="flex flex-col items-end gap-2">
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="secondary">
            {attempts[attempts.length - 1].cut_attempt_text}
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="w-max">
          {attempts.map((attempt) => (
            <>
              <DropdownMenuItem>{attempt.attempt_text}</DropdownMenuItem>
              <DropdownMenuItem>{attempt.cut_attempt_text}</DropdownMenuItem>
              <DropdownMenuSeparator />
            </>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  )
}
