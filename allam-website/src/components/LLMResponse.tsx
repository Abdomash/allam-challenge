import { Progress } from '@/lib/types'
import { cn } from '@/lib/utils'
import { Skeleton } from './ui/skeleton'
import CyclingText from './CyclingText'

interface LLMResponseProps {
  responses: Progress[]
  className?: string
}

const LoadingResponseTextAnimated: string[] = [
  'أفهم كلمات المستخدم',
  'أحدد الفكرة الرئيسية',
  'أنتج الكلمات المناسبة',
  'أبني البيت التالي',
  'أحلل وزن البيت',
  'أعد ضبط الإيقاع',
  'أقنن الكلمات لتتناسب مع الوزن',
  'أختار الصور الشعرية بعناية',
  'أعيد صياغة البيت ليصبح أكمل',
  'أراجع التراكيب اللغوية',
  'أصقل الكلمات لتصبح أكثر قوة',
]

export default function LLMResponse({
  responses,
  className,
}: LLMResponseProps) {
  return (
    <div className={cn('text-sm text-muted-foreground', className)}>
      {responses.map((response, i) => (
        <div key={i} className="flex flex-col gap-2">
          <p>{response.attempt_text}</p>
          <p>{response.aroodi_style}</p>
          <p>{response.wazn_comb}</p>
          <p>{response.wazn_mismatch}</p>
          <p>{response.cut_attempt_text}</p>
          <p>{response.is_last_attempt}</p>
        </div>
      ))}
      {responses.length === 0 && (
        <div className={cn('flex flex-col gap-2 items-end', className)}>
          <CyclingText
            className="pl-4"
            strings={LoadingResponseTextAnimated}
            interval={3000}
          />
          <Skeleton className="grid h-28 w-72 grid-cols-2 gap-4 rounded-md bg-secondary p-4">
            {Array.from(Array(6).keys()).map(() => (
              <Skeleton className="h-4 w-full rounded-md bg-gray-400" />
            ))}
          </Skeleton>
        </div>
      )}
    </div>
  )
}
