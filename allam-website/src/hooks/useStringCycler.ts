import { useState, useEffect } from 'react'

/**
 * A custom hook to cycle through a list of strings with a specified interval.
 *
 * @param strings - List of strings to cycle through.
 * @param interval - Time in milliseconds to show each string.
 * @returns The current string to display.
 */
export function useStringCycler(strings: string[], interval: number) {
  const [currentIndex, setCurrentIndex] = useState(0)

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % strings.length)
    }, interval)

    // Cleanup interval on component unmount
    return () => clearInterval(timer)
  }, [strings.length, interval])

  return strings[currentIndex]
}
