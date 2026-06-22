import type { Meta, StoryObj } from '@storybook/vue3-vite'
import BaseButton from '@/components/BaseButton.vue'

const meta = {
  title: 'Components/BaseButton',
  component: BaseButton,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
    a11y: {
      test: 'error',
    },
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'outline', 'brand-outline', 'danger', 'ghost'],
      description: 'Visual style variant',
    },
    loading: {
      control: 'boolean',
      description: 'Show loading spinner',
    },
    disabled: {
      control: 'boolean',
      description: 'Disable the button',
    },
    fullWidth: {
      control: 'boolean',
      description: 'Full width button',
    },
    type: {
      control: 'select',
      options: ['button', 'submit', 'reset'],
      description: 'Button type attribute',
    },
    default: {
      control: 'text',
      description: 'Button text content',
    },
  },
  args: {
    variant: 'primary',
    loading: false,
    disabled: false,
    fullWidth: false,
    type: 'button',
    default: 'Нажми меня',
  },
} satisfies Meta<typeof BaseButton>

export default meta
type Story = StoryObj<typeof meta>

export const Primary: Story = {
  args: {
    variant: 'primary',
    default: 'Присоединиться',
  },
}

export const Outline: Story = {
  args: {
    variant: 'outline',
    default: 'Отмена',
  },
}

export const BrandOutline: Story = {
  args: {
    variant: 'brand-outline',
    default: 'Открыть',
  },
}

export const Danger: Story = {
  args: {
    variant: 'danger',
    default: 'Удалить аккаунт',
  },
}

export const Ghost: Story = {
  args: {
    variant: 'ghost',
    default: 'Назад',
  },
}

export const Loading: Story = {
  args: {
    loading: true,
    default: 'Загрузка...',
  },
}

export const Disabled: Story = {
  args: {
    disabled: true,
    default: 'Недоступно',
  },
}

export const FullWidth: Story = {
  parameters: {
    layout: 'padded',
  },
  args: {
    fullWidth: true,
    default: 'На всю ширину',
  },
}

export const AllVariants: Story = {
  render: () => ({
    components: { BaseButton },
    template: `
      <div style="display: flex; flex-direction: column; gap: 16px; width: 360px;">
        <BaseButton variant="primary">Primary</BaseButton>
        <BaseButton variant="outline">Outline</BaseButton>
        <BaseButton variant="brand-outline">Brand Outline</BaseButton>
        <BaseButton variant="danger">Danger</BaseButton>
        <BaseButton variant="ghost">Ghost</BaseButton>
      </div>
    `,
  }),
}

export const States: Story = {
  render: () => ({
    components: { BaseButton },
    template: `
      <div style="display: flex; flex-direction: column; gap: 16px; width: 360px;">
        <BaseButton variant="primary">Normal</BaseButton>
        <BaseButton variant="primary" loading>Loading</BaseButton>
        <BaseButton variant="primary" disabled>Disabled</BaseButton>
      </div>
    `,
  }),
}

export const WithClickHandler: Story = {
  render: () => ({
    components: { BaseButton },
    template: `
      <BaseButton variant="primary" @click="onClick">
        Нажми меня
      </BaseButton>
    `,
    methods: {
      onClick() {
        alert('Button clicked!')
      },
    },
  }),
}
