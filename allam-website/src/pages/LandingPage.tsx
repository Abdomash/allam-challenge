import ChatView from '@/components/ChatView'
import RequestGenerationForm from '@/components/RequestGenerationForm'
import { DataProvider } from '@/providers/DataProvider'

export function LandingPage() {
  return (
    <DataProvider>
      <div className="flex h-screen flex-col items-center justify-center p-4">
        <h1 className="sticky mb-8 text-center text-4xl font-bold">
          الشاعر علام
        </h1>
        <ChatView className="flex-1 overflow-y-auto" />
        <RequestGenerationForm className="sticky bottom-4" />
      </div>
    </DataProvider>
  )
}
