<template>
  <div class="admin-orders">
    <h2 class="press-start p-1">Управление заказами</h2>

    <!-- Фильтры -->
    <div class="filters mb-4">
      <div class="row">
        <div class="col-md-4">
          <select v-model="statusFilter" class="form-select" @change="handleFilterChange">
            <option value="">Все статусы</option>
            <option value="new">Новый</option>
            <option value="processing">В обработке</option>
            <option value="completed">Выполнен</option>
            <option value="cancelled">Отменён</option>
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

    <!-- Список заказов -->
    <div v-else class="orders-list">
      <div v-for="order in orders" :key="order.id" class="order-card mb-4">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <div>
              <h5 class="mb-0">Заказ #{{ order.id }}</h5>
              <small class="text-muted">{{ formatDate(order.created_at) }}</small>
            </div>
            <div class="status-badge" :class="getStatusClass(order.status)">
              {{ getStatusText(order.status) }}
            </div>
          </div>
          
          <div class="card-body">
            <!-- Информация о пользователе -->
            <div class="user-info mb-3">
              <h6>Информация о покупателе:</h6>
              <div class="row">
                <div class="col-md-6">
                  <p><strong>Имя:</strong> {{ order.user.name || 'Не указано' }}</p>
                  <p><strong>Телефон:</strong> {{ order.user.phone || 'Не указан' }}</p>
                </div>
                <div class="col-md-6">
                  <p><strong>Email:</strong> {{ order.user.email || 'Не указан' }}</p>
                  <p><strong>Адрес:</strong> {{ order.user.address || 'Не указан' }}</p>
                </div>
              </div>
            </div>

            <!-- Товары -->
            <div class="order-items">
              <h6>Товары ({{ order.items_count }}):</h6>
              <ul class="list-group">
                <li v-for="(item, index) in order.items" 
                    :key="index"
                    class="list-group-item d-flex justify-content-between align-items-center"
                >
                  <div>
                    {{ item.name }}
                    <span v-if="item.variant" class="text-muted">
                      ({{ item.variant }})
                    </span>
                  </div>
                  <span>{{ formatPrice(item.price) }} ₽</span>
                </li>
              </ul>
              <div class="total-price mt-3 text-end">
                <strong>Итого: {{ formatPrice(order.total_price) }} ₽</strong>
              </div>
            </div>

            <!-- Действия -->
            <div class="order-actions mt-3">
              <select 
                v-model="order.status" 
                class="form-select d-inline-block w-auto me-2"
                @change="updateOrderStatus(order.id, $event.target.value)"
              >
                <option value="new">Новый</option>
                <option value="processing">В обработке</option>
                <option value="completed">Выполнен</option>
                <option value="cancelled">Отменён</option>
              </select>
            </div>
          </div>
        </div>
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { API_BASE_URL } from '../../config';
import axios from 'axios';

const orders = ref([]);
const loading = ref(true);
const error = ref(null);
const currentPage = ref(1);
const totalPages = ref(1);
const statusFilter = ref('');

const fetchOrders = async () => {
  try {
    loading.value = true;
    const response = await axios.get(`${API_BASE_URL}/api/admin/orders`, {
      params: {
        page: currentPage.value,
        status: statusFilter.value || undefined
      }
    });
    orders.value = response.data.items;
    totalPages.value = response.data.pages;
  } catch (err) {
    error.value = 'Ошибка при загрузке заказов';
    console.error('Ошибка:', err);
  } finally {
    loading.value = false;
  }
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('ru-RU');
};

const formatPrice = (price) => {
  return price.toLocaleString('ru-RU');
};

const getStatusText = (status) => {
  const statusMap = {
    'new': 'Новый',
    'processing': 'В обработке',
    'completed': 'Выполнен',
    'cancelled': 'Отменён'
  };
  return statusMap[status] || status;
};

const getStatusClass = (status) => {
  const classMap = {
    'new': 'status-new',
    'processing': 'status-processing',
    'completed': 'status-completed',
    'cancelled': 'status-cancelled'
  };
  return classMap[status] || '';
};

const updateOrderStatus = async (orderId, newStatus) => {
  try {
    await axios.put(`${API_BASE_URL}/api/admin/orders/${orderId}/status`, {
      status: newStatus
    });
    // Обновляем список заказов
    await fetchOrders();
  } catch (err) {
    console.error('Ошибка при обновлении статуса:', err);
  }
};

const changePage = (page) => {
  currentPage.value = page;
  fetchOrders();
};

const handleFilterChange = () => {
  currentPage.value = 1;
  fetchOrders();
};

onMounted(() => {
  fetchOrders();
});
</script>

<style scoped>
.admin-orders {
  padding: 20px;
}

.order-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9em;
}

.status-new {
  background-color: #e3f2fd;
  color: #1976d2;
}

.status-processing {
  background-color: #fff3e0;
  color: #f57c00;
}

.status-completed {
  background-color: #e8f5e9;
  color: #388e3c;
}

.status-cancelled {
  background-color: #ffebee;
  color: #d32f2f;
}

.user-info {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
}

.order-items {
  margin-top: 20px;
}

.total-price {
  font-size: 1.2em;
}

.order-actions {
  border-top: 1px solid #eee;
  padding-top: 15px;
}
</style>
