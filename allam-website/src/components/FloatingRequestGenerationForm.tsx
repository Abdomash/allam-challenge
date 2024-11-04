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
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { useForm } from 'react-hook-form'
import { ApiRequest, Bohours, Poets } from '@/types'

export default function FloatingRequestGenerationForm() {
  const form = useForm<ApiRequest>({
    defaultValues: {
      prompt: '',
      poet: 'علام',
      bahr: '--',
      poetryMode: true,
    },
  })

  const onSubmit = async (data: ApiRequest) => {
    await new Promise<void>((resolve) =>
      setTimeout(() => {
        resolve()
        form.reset()
        console.log('Form data:', data)
      }, 3000),
    )

    // TODO: Implement form submission
  }

  return (
    <div className="size-fit overflow-hidden rounded-lg bg-card shadow-lg md:max-w-3xl">
      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="flex h-full flex-row gap-4 p-4 md:flex-col"
        >
          <div className="items-center align-middle">
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
          </div>

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
            <FormField
              control={form.control}
              name="bahr"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>اختر البحر</FormLabel>
                  <FormControl>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <SelectTrigger
                        className="w-24"
                        disabled={form.formState.isSubmitting}
                      >
                        <SelectValue placeholder={field.value} />
                      </SelectTrigger>
                      <SelectContent>
                        {Bohours.map((bahr) => (
                          <SelectItem key={bahr} value={bahr}>
                            {bahr}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="poet"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>اختر الشاعر</FormLabel>
                  <FormControl>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <SelectTrigger
                        className="w-32"
                        disabled={form.formState.isSubmitting}
                      >
                        <SelectValue placeholder={field.value} />
                      </SelectTrigger>
                      <SelectContent>
                        {Poets.map((poet) => (
                          <SelectItem key={poet} value={poet}>
                            {poet}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
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
