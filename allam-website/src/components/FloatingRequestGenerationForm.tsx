import { useState } from 'react'
import { CircleChevronLeft } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Switch } from '@/components/ui/switch'
import { Label } from '@/components/ui/label'

const options = {
  bohours: ['الكامل', 'الطويل', 'البسيط', 'الوافر'],
  poets: ['امرؤ القيس', 'أحمد شوقي', 'المتنبي', 'عنترة بن شداد'],
}

const OptionMenu = ({
  htmlFor,
  label,
  placeholder,
  defaultItem,
  items,
}: {
  htmlFor: string
  label: string
  placeholder?: string
  defaultItem: string
  items: string[]
}) => {
  return (
    <div>
      <Label htmlFor={htmlFor} className="mx-1 text-sm font-medium">
        {label}
      </Label>
      <Select>
        <SelectTrigger className="w-[140px]">
          <SelectValue placeholder={placeholder ?? defaultItem} />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value={defaultItem}>
            {placeholder ?? defaultItem}
          </SelectItem>
          {items.map((item) => (
            <SelectItem key={item} value={item}>
              {item}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  )
}

const ToggleGenerationMode = ({
  htmlFor,
  label,
  checked,
  onCheckedChange,
}: {
  htmlFor: string
  label: string
  checked: boolean
  onCheckedChange: (checked: boolean) => void
}) => {
  return (
    <div className="flex flex-row items-center gap-1">
      <Label htmlFor={htmlFor}>{label}</Label>
      <Switch
        id={htmlFor}
        checked={checked}
        onCheckedChange={onCheckedChange}
      />
    </div>
  )
}

export default function FloatingRequestGenerationForm() {
  const [isGeneration, setIsGeneration] = useState(true)

  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    console.log('Form submitted')
    // TODO: Implement form submission
  }

  return (
    <div className="size-fit overflow-hidden rounded-lg bg-card shadow-lg md:max-w-3xl">
      <form
        onSubmit={onSubmit}
        className="flex h-full flex-row gap-4 p-4 md:flex-col"
      >
        <div className="items-center align-middle">
          <ToggleGenerationMode
            htmlFor="generation-mode"
            label={'نمط ' + (isGeneration ? 'الشاعر' : 'المحلّل')}
            checked={isGeneration}
            onCheckedChange={setIsGeneration}
          />
        </div>

        <div className="flex flex-col items-end justify-evenly gap-4 md:flex-row">
          <div>
            <Label htmlFor="poem">اكتب طلبك</Label>
            <Input placeholder="عطني قصيدة عن الوطن..." />
          </div>
          <OptionMenu
            htmlFor="bahr"
            label="اختر البحر"
            defaultItem="--"
            items={options.bohours}
          />
          <OptionMenu
            htmlFor="poet"
            label="اختر الشاعر"
            placeholder="علام"
            defaultItem="--"
            items={options.poets}
          />
          <Button type="submit" size="icon">
            <CircleChevronLeft className="size-4" />
          </Button>
        </div>
      </form>
    </div>
  )
}
