import { Button } from '@/components/ui/button'
import { Link } from 'react-router-dom'

export default function NotFoundPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4 p-4">
      <h1 className="mb-8 text-center text-4xl font-bold">الشاعر علّام</h1>
      <p className="text-center text-lg">404 - الصفحة غير موجودة</p>
      <Button asChild>
        <Link to="/">العودة إلى الصفحة الرئيسية</Link>
      </Button>
    </div>
  )
}
