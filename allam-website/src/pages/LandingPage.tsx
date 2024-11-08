import ChatView from '@/components/ChatView'
import RequestGenerationForm from '@/components/GenerationForm'
import { ChatLogProvider } from '@/providers/ChatLogContext'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient()

export function LandingPage() {
  return (
    <div className="flex h-screen flex-col items-center justify-center p-4">
      <h1 className="sticky mb-8 text-center text-4xl font-bold">
        الشاعر علام
      </h1>
      <QueryClientProvider client={queryClient}>
        <ChatLogProvider>
          <h1 className="text-center text-2xl font-bold">سجل المحادثة</h1>
          <ChatView className="flex-1 overflow-y-auto" />
          <RequestGenerationForm className="sticky bottom-4" />
        </ChatLogProvider>
      </QueryClientProvider>
    </div>
  )
}
