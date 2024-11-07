import { CircleChevronLeft } from 'lucide-react'
import { Button } from '@/components/ui/button'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { useForm, UseFormReturn } from 'react-hook-form'
import { Bohours, Poets } from '@/lib/constants'
import { cn } from '@/lib/utils'
import { ApiGenerateRequest } from '@/lib/types'
import { Input } from './ui/input'
import { useChatLog } from '@/hooks/useChatLog'
import { useMutation } from '@tanstack/react-query'

interface SelectMenuProps {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  form: UseFormReturn<ApiGenerateRequest, any, undefined>
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  name: any
  label: string
  items: string[]
}

function SelectMenu({ form, name, label, items }: SelectMenuProps) {
  return (
    <FormField
      control={form.control}
      name={name}
      render={({ field }) => (
        <FormItem>
          <FormLabel>{label}</FormLabel>
          <FormControl>
            <Select onValueChange={field.onChange} defaultValue={field.value}>
              <SelectTrigger
                className="w-32"
                disabled={form.formState.isSubmitting}
              >
                <SelectValue placeholder={field.value} />
              </SelectTrigger>
              <SelectContent>
                {items.map((item) => (
                  <SelectItem key={item} value={item}>
                    {item}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
  )
}

interface GenerationFormProps {
  className?: string
}

export default function GenerationForm({ className }: GenerationFormProps) {
  const form = useForm<ApiGenerateRequest>({
    defaultValues: {
      prompt: '',
      poet: 'علام',
      bahr: '--',
    },
  })

  const { addEntry, updateLastEntry } = useChatLog()

  const mutation = useMutation({
    mutationFn: async (data: ApiGenerateRequest) => {
      const response = await fetch('/api/generate', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
      return response.json()
    },
    onMutate: async (data) => {
      addEntry({ type: 'generate', request: data, response: undefined })
    },
    onSuccess: (responseData) => {
      updateLastEntry(responseData)
      form.reset()
    },
    onError: () => {
      updateLastEntry({
        type: 'error',
        request: form.getValues(),
        response: undefined,
      })
    },
  })

  const onSubmit = async (data: ApiGenerateRequest) => {
    await mutation.mutateAsync(data)
  }

  return (
    <div
      className={cn(
        'size-fit overflow-hidden rounded-lg bg-card shadow-lg md:max-w-3xl',
        className,
      )}
    >
      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="flex h-full flex-row gap-4 p-4 md:flex-col"
        >
          {/* <div className="items-center align-middle">
            <FormField
              control={form.control}
              name="poetryMode"
              render={({ field }) => (
                <FormItem className="flex flex-row items-start justify-start gap-1">
                  <FormControl>
                    <Switch
                      id="poetryMode"
                      checked={field.value}
                      onCheckedChange={field.onChange}
                      disabled={form.formState.isSubmitting}
                    />
                  </FormControl>
                  <FormLabel htmlFor="poetryMode">
                    {'نمط ' + (field.value ? 'الشاعر' : 'المحلّل')}
                  </FormLabel>
                </FormItem>
              )}
            />
          </div> */}

          <div className="flex flex-col items-end justify-evenly gap-4 md:flex-row">
            <FormField
              control={form.control}
              name="prompt"
              render={({ field }) => (
                <FormItem>
                  <FormLabel htmlFor="prompt">اكتب طلبك</FormLabel>
                  <FormControl>
                    <Input
                      {...field}
                      placeholder="عطني قصيدة عن الوطن..."
                      required
                      disabled={form.formState.isSubmitting}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <SelectMenu
              form={form}
              name="bahr"
              label="اختر البحر"
              items={Bohours}
            />
            <SelectMenu
              form={form}
              name="poet"
              label="اختر الشاعر"
              items={Poets}
            />

            <Button
              type="submit"
              size="icon"
              disabled={form.formState.isSubmitting}
            >
              <CircleChevronLeft className="size-4" />
            </Button>
          </div>
        </form>
      </Form>
    </div>
  )
}
