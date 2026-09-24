// 前端脱敏兜底（正常以后端返回为准，这里用于本地展示兜底）
export function maskPhone(phone) {
  if (!phone || phone.length < 7) return phone || ''
  return phone.slice(0, 3) + '****' + phone.slice(-4)
}

export function maskEmail(email) {
  if (!email || !email.includes('@')) return email || ''
  const [name, domain] = email.split('@')
  if (name.length <= 1) return '*@' + domain
  return name[0] + '***' + name.slice(-1) + '@' + domain
}
