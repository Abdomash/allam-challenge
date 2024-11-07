import ChatView from '@/components/ChatView'
import RequestGenerationForm from '@/components/GenerationForm'
import { ChatLogProvider } from '@/providers/ChatLogContext'

export function LandingPage() {
  return (
    <div className="flex h-screen flex-col items-center justify-center p-4">
      <h1 className="sticky mb-8 text-center text-4xl font-bold">
        الشاعر علام
      </h1>
      <ChatLogProvider>
        <ChatView className="flex-1 overflow-y-auto" />
        <RequestGenerationForm className="sticky bottom-4" />
      </ChatLogProvider>
    </div>
  )
}
