import { useStringCycler } from '@/hooks/useStringCycler'
import { cn } from '@/lib/utils'
import React from 'react'

interface CyclingTextProps {
  strings: string[]
  interval: number
  className?: string
}

const CyclingText: React.FC<CyclingTextProps> = ({
  strings,
  interval,
  className,
}) => {
  const currentString = useStringCycler(strings, interval)

  return (
    <div
      className={cn(
        'relative text-center font-bold opacity-100 transition-opacity duration-1000 ease-in-out',
        className,
      )}
    >
      {currentString}
    </div>
  )
}

export default CyclingText
