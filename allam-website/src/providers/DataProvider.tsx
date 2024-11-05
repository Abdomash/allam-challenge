import { DataContext } from '@/contexts/DataContext'
import { WEBSOCKET_URL } from '@/lib/constants'
import { ApiRequest, ApiResponse, DataEntry, Progress } from '@/lib/types'
import { useReducer, useEffect, useRef, PropsWithChildren } from 'react'

export interface DataState {
  dataById: { [key: string]: DataEntry }
}

export type DataAction =
  | {
      type: 'START_REQUEST'
      payload: { form_request_id: string; prompt: string }
    }
  | { type: 'ADD_DATA'; payload: { form_request_id: string; data: Progress } }
  | { type: 'END_REQUEST'; payload: { form_request_id: string } }

function dataReducer(state: DataState, action: DataAction): DataState {
  switch (action.type) {
    case 'START_REQUEST': {
      const { form_request_id, prompt } = action.payload
      return {
        ...state,
        dataById: {
          ...state.dataById,
          [form_request_id]: { prompt, responses: [] },
        },
      }
    }
    case 'ADD_DATA': {
      const { form_request_id: id, data } = action.payload
      const existingEntry = state.dataById[id]
      if (existingEntry) {
        return {
          ...state,
          dataById: {
            ...state.dataById,
            [id]: {
              ...existingEntry,
              responses: [...existingEntry.responses, data],
            },
          },
        }
      } else {
        // Handle the case where START_REQUEST was not dispatched
        return state
      }
    }
    case 'END_REQUEST':
      // Handle end of request if needed
      return state
    default:
      return state
  }
}

export interface StartRequestMessage {
  type: 'start_request'
  form_request_id: string
  formData: ApiRequest
}

const initialState: DataState = {
  dataById: JSON.parse(localStorage.getItem('dataById') || '{}'),
}

export function DataProvider({ children }: PropsWithChildren) {
  const [state, dispatch] = useReducer(dataReducer, initialState)
  const wsRef = useRef<WebSocket | null>(null)

  // Keep track of the latest state
  const stateRef = useRef(state)
  stateRef.current = state

  useEffect(() => {
    wsRef.current = new WebSocket(WEBSOCKET_URL)

    wsRef.current.onopen = () => {
      console.log('WebSocket connected')
    }

    wsRef.current.onmessage = (event) => {
      try {
        const message: ApiResponse = JSON.parse(event.data)
        const { request_id: form_request_id, data } = message

        dispatch({
          type: 'ADD_DATA',
          payload: { form_request_id, data },
        })

        if (data.is_last_attempt) {
          dispatch({
            type: 'END_REQUEST',
            payload: { form_request_id },
          })
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error)
      }
    }

    wsRef.current.onclose = () => {
      console.log('WebSocket disconnected')
    }

    return () => {
      wsRef.current?.close()
    }
  }, [])

  // Sync state with localStorage
  useEffect(() => {
    localStorage.setItem('dataById', JSON.stringify(state.dataById))
  }, [state.dataById])

  const sendMessage = (message: StartRequestMessage) => {
    dispatch({
      type: 'START_REQUEST',
      payload: {
        form_request_id: message.form_request_id,
        prompt: message.formData.prompt,
      },
    })

    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message))
    } else {
      console.error('WebSocket is not open, message captured:', message)
    }
  }

  return (
    <DataContext.Provider value={{ state, dispatch, sendMessage }}>
      {children}
    </DataContext.Provider>
  )
}
