import { Attempt } from '@/lib/types'
import { Button } from './ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuTrigger,
} from './ui/dropdown-menu'
import ColorizedText from './ColorizedText'

function ShatrInfo({ attempt }: { attempt: Attempt }) {
  const formatted_comb = attempt.wazn_comb
    .replace(new RegExp('0', 'g'), 'ه')
    .replace(new RegExp('1', 'g'), '/')

  return (
    <DropdownMenuItem>
      <DropdownMenuSub>
        <DropdownMenuSubTrigger className="w-full justify-end">
          <div className="w-full text-right">{attempt.attempt_text}</div>
        </DropdownMenuSubTrigger>
        <DropdownMenuSubContent>
          <DropdownMenuLabel className="text-center">الوزن</DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuItem>
            <ColorizedText
              className="text-right"
              text={'\u200f' + formatted_comb}
              mistakeIndex={attempt.wazn_mismatch}
            />
          </DropdownMenuItem>
          <DropdownMenuItem className="justify-center">
            {attempt.tf3elat === '(لم يعثر على تفعيلات)' ? (
              <span className="text-center">{attempt.tf3elat}</span>
            ) : (
              <ColorizedText
                text={attempt.tf3elat}
                mistakeIndex={attempt.wazn_mismatch}
              />
            )}
          </DropdownMenuItem>
        </DropdownMenuSubContent>
      </DropdownMenuSub>
    </DropdownMenuItem>
  )
}

export interface ShatrViewProps {
  attempts: Attempt[]
}

export default function ShatrView({ attempts }: ShatrViewProps) {
  // sort attempts by iteration number
  const sortedAttempts = [...attempts].sort(
    (a, b) => a.iteration_number - b.iteration_number,
  )

  return (
    <div className="min-w-8">
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="ghost" className="w-full text-justify">
            {sortedAttempts[sortedAttempts.length - 1].attempt_text}
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="w-max">
          <DropdownMenuLabel className="pb-1 text-center">
            المحاولات
          </DropdownMenuLabel>
          {sortedAttempts.map((attempt) => (
            <>
              <DropdownMenuSeparator />
              <ShatrInfo attempt={attempt} />
            </>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  )
}
