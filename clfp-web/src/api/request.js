import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '',
  timeout: 10000
})

// 请求拦截：自动带上 JWT
request.interceptors.request.use((config) => {
  const token = localStorage.getItem('clfp_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截：统一拆包、统一报错、401 自动跳登录
request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const status = error.response?.status
    const detail = error.response?.data?.detail || '网络异常，请稍后再试'

    if (status === 401) {
      localStorage.removeItem('clfp_token')
      ElMessage.error('登录已过期，请重新登录')
      router.push({ path: '/login', query: { redirect: router.currentRoute.value.fullPath } })
    } else {
      ElMessage.error(detail)
    }
    return Promise.reject(error)
  }
)

export default request
