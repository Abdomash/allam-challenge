export interface ColorizedTextProps {
  text: string
  colormap: string
}

export default function ColorizedText({ text, colormap }: ColorizedTextProps) {
  if (colormap.length === text.length) {
    console.error('Color map length must match text length')
    return <p>{text}</p>
  }

  const color_dictionary = {
    R: 'text-green-500',
    G: 'text-blue-500',
    B: 'text-red-500',
  }

  return (
    <div>
      {text.split('').map((char, i) => {
        return (
          <span
            key={i}
            className={color_dictionary[colormap[i] as 'R' | 'G' | 'B']}
          >
            {char}
          </span>
        )
      })}
    </div>
  )
}
