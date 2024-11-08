import { Attempt } from '@/lib/types'
import { Button } from './ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from './ui/dropdown-menu'
import ColorizedText from './ColorizedText'

export interface ShatrViewProps {
  attempts: Attempt[]
}

export default function ShatrView({ attempts }: ShatrViewProps) {
  // sort attempts by iteration number
  attempts.sort((a, b) => a.iteration_number - b.iteration_number)

  const lastAttempt = attempts[attempts.length - 1].attempt_text

  return (
    <div className="min-w-8">
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="ghost" className="w-full text-justify">
            {lastAttempt}
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="w-max">
          {attempts.map((attempt, i) => (
            <>
              {/* <DropdownMenuItem>{attempt.attempt_text}</DropdownMenuItem>
              <DropdownMenuItem>{attempt.cut_attempt_text}</DropdownMenuItem> */}
              <DropdownMenuItem className="justify-end">
                <ColorizedText
                  text={attempt.attempt_text}
                  mistakeIndex={attempt.wazn_mismatch}
                />
                {i + 1}
              </DropdownMenuItem>
              {i + 1 < attempts.length && <DropdownMenuSeparator />}
            </>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  )
}
