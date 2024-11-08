export interface ColorizedTextProps {
  text: string
  mistakeIndex: number
  className?: string
}

export default function ColorizedText({
  text,
  mistakeIndex,
  className,
}: ColorizedTextProps) {
  if (mistakeIndex < 0 || mistakeIndex >= text.length) {
    return <div>{text}</div>
  }

  const index_to_color = (idx: number) => {
    if (Math.abs(idx - mistakeIndex) <= 1) {
      return 'text-red-500'
    } else {
      return 'text-green-500'
    }
  }

  return (
    <div className={className}>
      {text.split('').map((char, i) => {
        return (
          <span key={i} className={index_to_color(i)}>
            {char}
          </span>
        )
      })}
    </div>
  )
}
