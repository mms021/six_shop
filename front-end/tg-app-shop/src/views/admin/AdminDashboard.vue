<template>
  <div class="admin-dashboard">
    <h2 class="press-start p-1">Панель управления</h2>

    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>

    <div v-else class="dashboard-content">
      <!-- Основные показатели -->
      <div class="row">
        <!-- Товары -->
        <div class="col-md-3 mb-4">
          <div class="stat-card">
            <div class="stat-card-header">
              <h3>Товары</h3>
            </div>
            <div class="stat-card-body">
              <div class="stat-item">
                <span class="stat-label">Всего:</span>
                <span class="stat-value">{{ stats.products.total }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Активных:</span>
                <span class="stat-value">{{ stats.products.active }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Категории -->
        <div class="col-md-3 mb-4">
          <div class="stat-card">
            <div class="stat-card-header">
              <h3>Категории</h3>
            </div>
            <div class="stat-card-body">
              <div class="stat-item">
                <span class="stat-label">Всего:</span>
                <span class="stat-value">{{ stats.categories.total }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Заказы -->
        <div class="col-md-3 mb-4">
          <div class="stat-card">
            <div class="stat-card-header">
              <h3>Заказы</h3>
            </div>
            <div class="stat-card-body">
              <div class="stat-item">
                <span class="stat-label">Всего:</span>
                <span class="stat-value">{{ stats.orders.total }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">За 30 дней:</span>
                <span class="stat-value">{{ stats.orders.recent }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Выручка -->
        <div class="col-md-3 mb-4">
          <div class="stat-card">
            <div class="stat-card-header">
              <h3>Выручка</h3>
            </div>
            <div class="stat-card-body">
              <div class="stat-item">
                <span class="stat-label">Общая:</span>
                <span class="stat-value">{{ formatPrice(stats.revenue.total) }} ₽</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">За 30 дней:</span>
                <span class="stat-value">{{ formatPrice(stats.revenue.recent) }} ₽</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Популярные категории -->
      <div class="row mt-4">
        <div class="col-md-6">
          <div class="stat-card">
            <div class="stat-card-header">
              <h3>Популярные категории</h3>
            </div>
            <div class="stat-card-body">
              <div 
                v-for="category in stats.categories.popular" 
                :key="category.name"
                class="popular-category"
              >
                <span class="category-name">{{ category.name }}</span>
                <span class="category-count">{{ category.count }} товаров</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { API_BASE_URL } from '../../config';
import axios from 'axios';

const stats = ref({
  products: { total: 0, active: 0 },
  categories: { total: 0, popular: [] },
  orders: { total: 0, recent: 0 },
  revenue: { total: 0, recent: 0 }
});
const loading = ref(true);
const error = ref(null);

const fetchStatistics = async () => {
  try {
    loading.value = true;
    const response = await axios.get(`${API_BASE_URL}/api/admin/statistics`);
    stats.value = response.data;
  } catch (err) {
    error.value = 'Ошибка при загрузке статистики';
    console.error('Ошибка:', err);
  } finally {
    loading.value = false;
  }
};

const formatPrice = (price) => {
  return price.toLocaleString('ru-RU');
};

onMounted(() => {
  fetchStatistics();
});
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
}

.stat-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  height: 100%;
}

.stat-card-header {
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.stat-card-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
}

.stat-card-body {
  padding: 15px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.stat-item:last-child {
  margin-bottom: 0;
}

.stat-label {
  color: #666;
}

.stat-value {
  font-weight: bold;
  color: #333;
}

.popular-category {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.popular-category:last-child {
  border-bottom: none;
}

.category-name {
  color: #333;
}

.category-count {
  color: #666;
  font-size: 0.9em;
}
</style> 