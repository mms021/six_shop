<template>
  <div class="search-container">
    <div class="input-group">
      <input
        type="text"
        class="form-control"
        v-model="searchQuery"
        @input="onSearch"
        @focus="showSuggestions = true"
        placeholder="Поиск товаров..."
      />
      <button class="btn btn-outline-secondary" @click="search" >
        <i class="bi bi-search"></i>
      </button>
    </div>
    
    <!-- Автоподсказки -->
    <div class="suggestions-container" v-if="showSuggestions && suggestions.length > 0">
      <ul class="suggestions-list">
        <li 
          v-for="suggestion in suggestions" 
          :key="suggestion.id"
          @click="selectSuggestion(suggestion)"
          class="suggestion-item"
        >
          <div class="d-flex align-items-center">
            <img :src="suggestion.image" class="suggestion-image" v-if="suggestion.image"/>
            <div class="suggestion-info">
              <div class="suggestion-name">{{ suggestion.name }}</div>
              <div class="suggestion-price">{{ suggestion.price }} ₽</div>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { API_BASE_URL } from '../config'

const router = useRouter()
const searchQuery = ref('')
const suggestions = ref([])
const showSuggestions = ref(false)
let debounceTimer = null

const onSearch = () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(async () => {
    if (searchQuery.value.length >= 2) {
      try {
        const response = await fetch(
          `${API_BASE_URL}/api/search?q=${encodeURIComponent(searchQuery.value)}`
        )
        const data = await response.json()
        suggestions.value = data.suggestions
      } catch (error) {
        console.error('Ошибка поиска:', error)
      }
    } else {
      suggestions.value = []
    }
  }, 300) // Задержка 300мс
}

const selectSuggestion = (suggestion) => {
  searchQuery.value = suggestion.name
  showSuggestions.value = false
  router.push(`/product/${suggestion.id}`)
}

const search = () => {
  if (searchQuery.value) {
    router.push(`/search?q=${encodeURIComponent(searchQuery.value)}`)
    showSuggestions.value = false
  }
}

// Закрываем подсказки при клике вне компонента
const handleClickOutside = (event) => {
  if (!event.target.closest('.search-container')) {
    showSuggestions.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.search-container {
  position: relative;
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}

.suggestions-container {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  z-index: 1000;
  max-height: 300px;
  overflow-y: auto;
}

.suggestions-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.suggestion-item {
  padding: 10px;
  cursor: pointer;
  border-bottom: 1px solid #eee;
}

.suggestion-item:hover {
  background-color: #f8f9fa;
}

.suggestion-image {
  width: 40px;
  height: 40px;
  object-fit: cover;
  margin-right: 10px;
  border-radius: 4px;
}

.suggestion-info {
  flex-grow: 1;
}

.suggestion-name {
  font-weight: 500;
}

.suggestion-price {
  font-size: 0.9em;
  color: #666;
}
</style> 