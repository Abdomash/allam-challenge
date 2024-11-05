import { Bohours, Poets } from './constants'

export interface DataEntry {
  prompt: string
  responses: Progress[]
}

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
  data: Progress
}

export interface ApiRequest {
  prompt: string
  poet: Poet
  bahr: Bahr
  poetryMode: boolean
}

export type Poet = (typeof Poets)[number]
export type Bahr = (typeof Bohours)[number]
