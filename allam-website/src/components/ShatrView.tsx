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
import { format_combinations } from '@/lib/utils'
import React from 'react'

function ShatrInfo({ attempt }: { attempt: Attempt }) {
  return (
    <DropdownMenuItem>
      <DropdownMenuSub>
        <DropdownMenuSubTrigger className="w-full justify-end">
          <span className="w-full text-right">{attempt.attempt_text}</span>
        </DropdownMenuSubTrigger>
        <DropdownMenuSubContent>
          <DropdownMenuLabel className="text-center">الوزن</DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuItem>
            <ColorizedText
              className="text-right"
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
        </DropdownMenuSubContent>
      </DropdownMenuSub>
    </DropdownMenuItem>
  )
}

export interface ShatrViewProps {
  attempts: Attempt[]
}

export default function ShatrView({ attempts }: ShatrViewProps) {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="w-full text-justify">
          {attempts[attempts.length - 1].attempt_text}
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-max">
        <DropdownMenuLabel className="pb-1 text-center">
          المحاولات
        </DropdownMenuLabel>
        {attempts.map((attempt, i) => (
          <React.Fragment key={i}>
            <DropdownMenuSeparator />
            <ShatrInfo attempt={attempt} />
          </React.Fragment>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
