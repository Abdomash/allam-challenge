import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function generateRandomId(): string {
  return Date.now().toString()
}

export function format_combinations(text: string): string {
  return text.replace(/0/g, 'ه').replace(/1/g, '/')
}
