import { ref } from 'vue'
import { API_BASE_URL } from '../config'

export function useAuth() {
  const user = ref(null)
  const webApp = window.Telegram?.WebApp

  const fetchUserInfo = async () => {
    if (!webApp?.initDataUnsafe?.user) {
      return null
    }

    const { id: tg_id, first_name, last_name, username, language_code } = webApp.initDataUnsafe.user
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/users/${tg_id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Telegram-Data': webApp.initData
        },
        body: JSON.stringify({
          tg_id,
          first_name,
          last_name,
          username,
          language_code
        })
      })
      
      if (!response.ok) {
        throw new Error('Ошибка авторизации')
      }

      const userData = await response.json()
      user.value = userData
      return userData
      
    } catch (error) {
      console.error('Ошибка при получении данных пользователя:', error)
      return null
    }
  }

  const checkAuth = async () => {
    if (!user.value) {
      await fetchUserInfo()
      if (!user.value) {
        throw new Error('Требуется авторизация')
      }
    }
    return user.value
  }

  return {
    user,
    fetchUserInfo,
    checkAuth
  }
} 