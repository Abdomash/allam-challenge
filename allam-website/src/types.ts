export interface Progress {
  shatr_number: number
  iteration_number: number
  attempt_text: string
  aroodi_style: string
  wazn_comb: string
  wazn_mismatch: string
  cut_attempt_text: string
  is_last_attempt: boolean
}

export interface ApiResponse {
  request_id: string
  progression: Progress[]
}

export interface ApiRequest {
  prompt: string
  poet: Poet
  bahr: Bahr | undefined
  poetryMode: boolean
}

export const Poets: string[] = [
  'علام',
  'امرؤ القيس',
  'أحمد شوقي',
  'المتنبي',
  'عنترة بن شداد',
] as const

export const Bohours: string[] = [
  '--',
  'الكامل',
  'الطويل',
  'البسيط',
  'الوافر',
] as const

export type Poet = (typeof Poets)[number]
export type Bahr = (typeof Bohours)[number]
