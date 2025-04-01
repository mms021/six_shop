<template>
  <div class="category-view">
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>

    <div v-else>
      <!-- Заголовок категории -->
      <h1 class="press-start p-1">{{ categoryData.category.name }}</h1>
      <hr class="p-1">

      <!-- Подкатегории -->
      <div v-if="categoryData.subcategories.length > 0" class="subcategories-section">
        <h2 class="press-start p-1">Подкатегории</h2>
        <div class="row">
          <div v-for="subcategory in categoryData.subcategories" 
               :key="subcategory.id" 
               class="col-6 col-md-4 mb-3">
            <router-link :to="`/category/${subcategory.id}`" class="subcategory-card">
              <div class="card">
                <img :src="subcategory.image || 'placeholder.jpg'" 
                     :alt="subcategory.name" 
                     class="card-img-top">
                <div class="card-body">
                  <h5 class="card-title">{{ subcategory.name }}</h5>
                </div>
              </div>
            </router-link>
          </div>
        </div>
        <hr class="p-1">
      </div>

      <!-- Товары -->
      <div class="products-section">
        <h2 class="press-start p-1" v-if="categoryData.subcategories.length > 0">
          Товары в этой категории
        </h2>
        <ProductsList :products="categoryData.products" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { API_BASE_URL, STATIC_URL } from '../config';
import { useAuth } from '../composables/useAuth';
import ProductsList from '@/components/ProductsList.vue';

const route = useRoute();
const { user } = useAuth();
const categoryData = ref({
  category: {},
  subcategories: [],
  products: []
});
const loading = ref(true);
const error = ref(null);

const fetchCategoryData = async () => {
  try {
    loading.value = true;
    const response = await axios.get(
      `${API_BASE_URL}/api/categories/${route.params.id}?user_id=${user.value?.id || ''}`
    );
    categoryData.value = response.data;
  } catch (err) {
    error.value = 'Ошибка при загрузке категории';
    console.error('Ошибка:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchCategoryData();
});

// Обновляем данные при изменении ID категории
watch(() => route.params.id, () => {
  fetchCategoryData();
});

const getFullImageUrl = (path) => {
  if (!path) return '';
  // Если путь уже содержит полный URL, возвращаем его как есть
  if (path.startsWith('http')) return path;
  // Иначе добавляем базовый URL для статических файлов
  return `${STATIC_URL}${path}`;
}
</script>

<style scoped>
.category-view {
  padding: 20px;
}

.subcategory-card {
  text-decoration: none;
  color: inherit;
}

.subcategory-card:hover {
  text-decoration: none;
}

.subcategory-card .card {
  transition: transform 0.2s;
}

.subcategory-card .card:hover {
  transform: translateY(-5px);
}

.card-img-top {
  height: 150px;
  object-fit: cover;
}

.card-title {
  font-size: 1rem;
  text-align: center;
  margin-bottom: 0;
}
</style>    