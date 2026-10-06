import request from './request'

export const getMe = () => request.get('/api/user/me')

export const updateMe = (data) => request.put('/api/user/me', data)

export const changePassword = (data) => request.post('/api/user/change-password', data)

export const getMyItems = (params) => request.get('/api/item/mine', { params })

export const getMyStats = () => request.get('/api/user/me/stats')

export const getContact = (userId) => request.get(`/api/user/contact/${userId}`)
