import { Attempt } from '@/lib/types'
import { Button } from './ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from './ui/dropdown-menu'
import ColorizedText from './ColorizedText'
import { format_combinations } from '@/lib/utils'

export interface ShatrViewProps {
  attempt: Attempt
}

export default function ShatrView({ attempt }: ShatrViewProps) {
  return (
    <div className="min-w-8">
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant="ghost"
            className="w-full text-justify hover:bg-[#cf9f5c]"
          >
            {attempt.attempt_text}
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="w-max">
          <DropdownMenuLabel className="text-center">الوزن</DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuItem className="justify-center">
            <ColorizedText
              className="justify-center text-center"
              text={'\u200f' + format_combinations(attempt.wazn_comb)}
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
          {attempt.feedback && (
            <>
              <DropdownMenuSeparator />
              <DropdownMenuLabel className="text-center">
                التحليل
              </DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem className="max-w-96 justify-end">
                {'\u200f' + attempt.feedback}
              </DropdownMenuItem>
            </>
          )}
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  )
}
