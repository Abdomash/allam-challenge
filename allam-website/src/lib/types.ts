import { Bohours, Poets } from './constants'

export type ResponseType = 'generate' | 'analyze' | 'error'

export interface ChatEntry {
  type: ResponseType
  request: ApiGenerateRequest | ApiAnalyzeRequest
  response: ApiGenerateResponse | ApiAnalyzeResponse | undefined
}

export type Attempt = {
  shatr_idx: number
  iteration_number: number
  attempt_text: string
  aroodi_style: string
  wazn_comb: string
  wazn_mismatch: number
  cut_attempt_text: string
}

export type ApiGenerateResponse = {
  type: 'generate'
  attempts: Attempt[]
}

export type ApiGenerateRequest = {
  type: 'generate'
  prompt: string
  poet: Poet
  bahr: Bahr
}

export type ApiAnalyzeRequest = {
  type: 'analyze'
  shatrs: string[]
}

export type AnalyzedShatr = {
  feedback: string
  shatr_text: string
  wazn_comb: string
  wazn_mismatch: string
}

export type ApiAnalyzeResponse = {
  type: 'analyze'
  analyzed_shatrs: AnalyzedShatr[]
}

export type Poet = (typeof Poets)[number]
export type Bahr = (typeof Bohours)[number]
