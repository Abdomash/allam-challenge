export interface ColorizedTextProps {
  text: string
  mistakeIndex: number
}

export default function ColorizedText({
  text,
  mistakeIndex,
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
    <div>
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
