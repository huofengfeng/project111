/**
 * 将相对路径的图片 URL 转为绝对路径（拼接后端 BASE_URL）
 * - 如果已经是 http/https 绝对路径，直接返回
 * - 如果是 / 开头的相对路径，拼接 VITE_BASE_URL
 * - 如果为空或无效，返回空字符串
 */
export function getImageUrl(url) {
  if (!url) return ''
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url
  }
  if (url.startsWith('/')) {
    return import.meta.env.VITE_BASE_URL + url
  }
  return url
}