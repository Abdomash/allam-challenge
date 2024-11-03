import FloatingRequestGenerationForm from '@/components/FloatingRequestGenerationForm'

export function LandingPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-4">
      <h1 className="mb-8 text-center text-4xl font-bold">الشاعر علام</h1>
      <FloatingRequestGenerationForm />
    </div>
  )
}
