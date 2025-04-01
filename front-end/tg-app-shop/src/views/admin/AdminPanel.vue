<template>
  <div class="admin-panel">
    <h2 class="press-start p-1">Панель управления</h2>

    <!-- Кнопки навигации -->
    <div class="admin-nav mb-4">
      <div class="row g-3">
        <!-- Товары -->
        <div class="col-md-3">
          <div class="dropdown">
            <button class="btn btn-primary w-100 d-flex align-items-center justify-content-between" 
                    type="button" 
                    data-bs-toggle="dropdown" 
                    aria-expanded="false">
              <span><i class="bi bi-box"></i> Товары</span>
              <i class="bi bi-chevron-down"></i>
            </button>
            <ul class="dropdown-menu w-100">
              <li>
                <router-link to="/admin-page/create-product" class="dropdown-item">
                  <i class="bi bi-plus-circle"></i> Добавить товар
                </router-link>
              </li>
              <li><hr class="dropdown-divider"></li>
              <li>
                <a class="dropdown-item" href="#" @click.prevent="showHiddenProducts">
                  <i class="bi bi-eye-slash"></i> Скрытые товары
                </a>
              </li>
              <li>
                <a class="dropdown-item" href="#" @click.prevent="showOutOfStock">
                  <i class="bi bi-exclamation-circle"></i> Нет в наличии
                </a>
              </li>
            </ul>
          </div>
        </div>

        <!-- Категории -->
        <div class="col-md-3">
          <div class="dropdown">
            <button class="btn btn-info w-100 d-flex align-items-center justify-content-between" 
                    type="button" 
                    data-bs-toggle="dropdown" 
                    aria-expanded="false">
              <span><i class="bi bi-folder"></i> Категории</span>
              <i class="bi bi-chevron-down"></i>
            </button>
            <ul class="dropdown-menu w-100">
              <li>
                <router-link to="/admin-page/categories" class="dropdown-item">
                  <i class="bi bi-list"></i> Список категорий
                </router-link>
              </li>
              <li>
                <router-link to="/admin-page/create-category" class="dropdown-item">
                  <i class="bi bi-plus-circle"></i> Добавить категорию
                </router-link>
              </li>
            </ul>
          </div>
        </div>

        <!-- Заказы -->
        <div class="col-md-3">
          <div class="dropdown">
            <button class="btn btn-success w-100 d-flex align-items-center justify-content-between" 
                    type="button" 
                    data-bs-toggle="dropdown" 
                    aria-expanded="false">
              <span><i class="bi bi-cart"></i> Заказы</span>
              <i class="bi bi-chevron-down"></i>
            </button>
            <ul class="dropdown-menu w-100">
              <li>
                <router-link to="/admin-page/orders" class="dropdown-item">
                  <i class="bi bi-list-check"></i> Все заказы
                </router-link>
              </li>
              <li>
                <a class="dropdown-item" href="#" @click.prevent="showNewOrders">
                  <i class="bi bi-bell"></i> Новые
                  <span class="badge bg-danger ms-2" v-if="newOrdersCount">{{ newOrdersCount }}</span>
                </a>
              </li>
            </ul>
          </div>
        </div>

        <!-- Аналитика -->
        <div class="col-md-3">
          <div class="dropdown">
            <button class="btn btn-warning w-100 d-flex align-items-center justify-content-between" 
                    type="button" 
                    data-bs-toggle="dropdown" 
                    aria-expanded="false">
              <span><i class="bi bi-graph-up"></i> Аналитика</span>
              <i class="bi bi-chevron-down"></i>
            </button>
            <ul class="dropdown-menu w-100">
              <li>
                <router-link to="/admin-page/dashboard" class="dropdown-item">
                  <i class="bi bi-speedometer2"></i> Дашборд
                </router-link>
              </li>
              <li>
                <a class="dropdown-item" href="#" @click.prevent="showStatistics">
                  <i class="bi bi-bar-chart"></i> Статистика продаж
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Фильтры и поиск -->
    <div class="filters mb-4">
      <div class="row g-3">
        <div class="col-md-4">
          <input 
            v-model="searchQuery" 
            type="text" 
            class="form-control"
            placeholder="Поиск по названию..."
            @input="handleSearch"
          >
        </div>
        <div class="col-md-4">
          <select v-model="categoryFilter" class="form-select" @change="handleSearch">
            <option value="">Все категории</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Загрузка -->
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
    </div>

    <!-- Ошибка -->
    <div v-else-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>

    <!-- Таблица товаров -->
    <div v-else class="table-responsive">
      <table class="table table-hover">
        <thead>
          <tr>
            <th>ID</th>
            <th>Изображение</th>
            <th>Название</th>
            <th>Категория</th>
            <th>Цена</th>
            <th>Старая цена</th>
            <th>Видимость</th>
            <th>Дата создания</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id">
            <td>{{ product.id }}</td>
            <td>
              <img 
                :src="product.image" 
                :alt="product.name"
                class="product-thumbnail"
                v-if="product.image"
              >
            </td>
            <td>{{ product.name }}</td>
            <td>{{ product.category }}</td>
            <td>{{ formatPrice(product.price) }} ₽</td>
            <td>{{ formatPrice(product.old_price) }} ₽</td>
            <td>
              <button 
                @click="toggleVisibility(product)" 
                class="btn"
                :class="product.visibility ? 'btn-success' : 'btn-secondary'"
              >
                {{ product.visibility ? 'Активен' : 'Скрыт' }}
              </button>
            </td>
            <td>{{ formatDate(product.created_at) }}</td>
            <td>
              <div class="btn-group">
                <router-link 
                  :to="`/admin-page/edit-product/${product.id}`" 
                  class="btn btn-sm btn-primary"
                >
                  <i class="bi bi-pencil"></i>
                </router-link>
                <button 
                  @click="deleteProduct(product.id)" 
                  class="btn btn-sm btn-danger"
                >
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Пагинация -->
    <nav v-if="totalPages > 1" class="mt-4">
      <ul class="pagination justify-content-center">
        <li 
          v-for="page in totalPages" 
          :key="page"
          class="page-item"
          :class="{ active: currentPage === page }"
        >
          <button 
            class="page-link" 
            @click="changePage(page)"
          >
            {{ page }}
          </button>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { API_BASE_URL } from '../../config';
import axios from 'axios';

const products = ref([]);
const categories = ref([]);
const loading = ref(true);
const error = ref(null);
const currentPage = ref(1);
const totalPages = ref(1);
const searchQuery = ref('');
const categoryFilter = ref('');

const fetchProducts = async () => {
  try {
    loading.value = true;
    const response = await axios.get(`${API_BASE_URL}/api/admin/products/list`, {
      params: {
        page: currentPage.value,
        search: searchQuery.value || undefined,
        category_id: categoryFilter.value || undefined
      }
    });
    products.value = response.data.items;
    totalPages.value = response.data.pages;
  } catch (err) {
    error.value = 'Ошибка при загрузке товаров';
    console.error('Ошибка:', err);
  } finally {
    loading.value = false;
  }
};

const fetchCategories = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/categories`);
    categories.value = response.data;
  } catch (err) {
    console.error('Ошибка при загрузке категорий:', err);
  }
};

const formatPrice = (price) => {
  return price.toLocaleString('ru-RU');
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('ru-RU');
};

const toggleVisibility = async (product) => {
  try {
    const response = await axios.put(
      `${API_BASE_URL}/api/admin/products/${product.id}/visibility`
    );
    product.visibility = response.data.visibility;
  } catch (err) {
    console.error('Ошибка при изменении видимости:', err);
  }
};

const deleteProduct = async (id) => {
  if (!confirm('Вы уверены, что хотите удалить этот товар?')) return;

  try {
    await axios.delete(`${API_BASE_URL}/api/admin/products/${id}`);
    await fetchProducts();
  } catch (err) {
    console.error('Ошибка при удалении товара:', err);
  }
};

const changePage = (page) => {
  currentPage.value = page;
  fetchProducts();
};

const handleSearch = () => {
  currentPage.value = 1;
  fetchProducts();
};

onMounted(() => {
  fetchCategories();
  fetchProducts();
});
</script>

<style scoped>
.admin-panel {
  padding: 20px;
}

.product-thumbnail {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 4px;
}

.table th {
  white-space: nowrap;
}

.btn-group {
  white-space: nowrap;
}

.filters {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
}

.action-buttons .btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.action-buttons i {
  font-size: 1.2em;
}
</style>
