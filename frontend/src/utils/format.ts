export function getStars(assessment: number): string {
  return '★'.repeat(assessment) + '☆'.repeat(5 - assessment)
}

export function formatDate(dateString?: string): string {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
}
