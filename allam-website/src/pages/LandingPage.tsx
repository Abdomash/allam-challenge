import ChatView from '@/components/ChatView'
import FloatingRequestGenerationForm from '@/components/FloatingRequestGenerationForm'
import { DataProvider } from '@/providers/DataProvider'

export function LandingPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-4">
      <h1 className="mb-8 text-center text-4xl font-bold">الشاعر علام</h1>
      <DataProvider>
        <ChatView />
        <FloatingRequestGenerationForm />
      </DataProvider>
    </div>
  )
}
