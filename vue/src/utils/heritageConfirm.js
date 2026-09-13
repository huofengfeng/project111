import { createApp, h } from 'vue'
import HeritageDialog from '@/components/HeritageDialog.vue'

export default function heritageConfirm({
  title = '提示',
  message = '',
  confirmText = '确认',
  cancelText = '取消',
}) {
  return new Promise((resolve) => {
    const container = document.createElement('div')
    document.body.appendChild(container)

    const app = createApp({
      render() {
        return h(HeritageDialog, {
          modelValue: visible.value,
          title,
          message,
          confirmText,
          cancelText,
          'onUpdate:modelValue': (val) => { visible.value = val },
          onConfirm: () => {
            resolve(true)
            cleanup()
          },
          onCancel: () => {
            resolve(false)
            cleanup()
          },
        })
      },
    })

    const visible = { value: true }
    app.mount(container)

    const cleanup = () => {
      visible.value = false
      setTimeout(() => {
        app.unmount()
        document.body.removeChild(container)
      }, 350)
    }
  })
}