<template>
  <div class="favorites">
    <h1 class="press-start p-1 text-center">Мои любимые товары</h1>
    
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>

    <div v-else-if="favoriteItems.length === 0" class="text-center press-start p-5">
      У вас пока нет любимых товаров.
    </div>
    
    <div v-else>
      <ProductsList :products="favoriteItems" @remove="removeFromFavorites" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { API_BASE_URL } from '../config';
import ProductsList from '@/components/ProductsList.vue';
import axios from 'axios';
import { useAuth } from '../composables/useAuth';

const { user } = useAuth();
const favoriteItems = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchFavorites = async () => {
  try {
    loading.value = true;
    const response = await axios.get(`${API_BASE_URL}/api/favorites?user_id=${user.value.id}`);
    favoriteItems.value = response.data;
  } catch (err) {
    error.value = 'Ошибка при загрузке избранных товаров';
    console.error('Ошибка:', err);
  } finally {
    loading.value = false;
  }
};

const removeFromFavorites = async (productId) => {
  try {
    await axios.post(`${API_BASE_URL}/api/like`, {
      userId: user.value.id,
      productId: productId
    });
    // Обновляем список после удаления
    favoriteItems.value = favoriteItems.value.filter(item => item.id !== productId);
  } catch (err) {
    console.error('Ошибка при удалении из избранного:', err);
  }
};

onMounted(() => {
  fetchFavorites();
});
</script>

<style>
.favorites {
  padding: 20px;
}
.favorite-item {
  margin: 10px 0;
}
</style> 