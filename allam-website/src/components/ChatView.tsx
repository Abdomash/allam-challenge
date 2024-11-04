import { useDataContext } from '@/hooks/useDataContext'
import React from 'react'

const ChatView: React.FC = () => {
  const dataContext = useDataContext()
  const { dataById } = dataContext.state

  return (
    <div>
      {Object.keys(dataById).map((form_request_id) => (
        <div key={form_request_id}>
          <h3>Request ID: {form_request_id}</h3>
          {dataById[form_request_id].map((progress, index) => (
            <div key={index}>
              <p>Attempt Text: {progress.attempt_text}</p>
              <p>Shatr Number: {progress.shatr_number}</p>
              <p>Iteration Number: {progress.iteration_number}</p>
              <p>Aroodi Style: {progress.aroodi_style}</p>
              <p>Wazn Comb: {progress.wazn_comb}</p>
              <p>Wazn Mismatch: {progress.wazn_mismatch}</p>
              <p>Cut Attempt Text: {progress.cut_attempt_text}</p>
              <p>Is Last Attempt: {progress.is_last_attempt ? 'Yes' : 'No'}</p>
            </div>
          ))}
        </div>
      ))}
    </div>
  )
}

export default ChatView
