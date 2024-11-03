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
