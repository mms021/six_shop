<template>
  <div class="order-history">
    <div class="header">
      <h1>История заказов</h1>
      <button class="back-btn" @click="$router.push('/cart')">
        Назад в корзину
      </button>
    </div>

    <div v-if="loading" class="loading">
      Загрузка...
    </div>

    <div v-else-if="orders.length === 0" class="empty">
      У вас пока нет заказов
    </div>

    <div v-else class="orders-list">
      <div v-for="order in orders" :key="order.id" class="order-card">
        <div class="order-header">
          <span class="order-number">Заказ #{{ order.id }}</span>
          <span :class="['order-status', order.status]">{{ getStatusText(order.status) }}</span>
        </div>

        <div class="order-date">
          {{ formatDate(order.created_at) }}
        </div>

        <div class="order-items">
          <div v-for="item in order.items" :key="item.id" class="order-item">
            <img :src="item.image" :alt="item.name" class="item-image">
            <div class="item-details">
              <div class="item-name">{{ item.name }}</div>
              <div class="item-variant">Размер: {{ item.variant }}</div>
              <div class="item-price">{{ formatPrice(item.price) }} ₽</div>
            </div>
          </div>
        </div>

        <div class="order-total">
          Итого: {{ formatPrice(order.total) }} ₽
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OrderHistory',
  data() {
    return {
      orders: [],
      loading: true
    }
  },
  
  async created() {
    await this.loadOrders()
  },
  
  methods: {
    async loadOrders() {
      try {
        const response = await this.$axios.get('/api/orders/history')
        this.orders = response.data
      } catch (error) {
        console.error('Ошибка при загрузке истории заказов:', error)
      } finally {
        this.loading = false
      }
    },
    
    getStatusText(status) {
      const statuses = {
        'new': 'Новый',
        'processing': 'В обработке',
        'completed': 'Выполнен',
        'cancelled': 'Отменён'
      }
      return statuses[status] || status
    },
    
    formatDate(date) {
      return new Date(date).toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    
    formatPrice(price) {
      return price.toLocaleString('ru-RU')
    }
  }
}
</script>

<style scoped>
.order-history {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.back-btn {
  padding: 8px 16px;
  background: #f0f0f0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.loading,
.empty {
  text-align: center;
  padding: 40px;
  color: #666;
}

.order-card {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.order-number {
  font-weight: bold;
}

.order-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
}

.order-status.new { background: #e3f2fd; }
.order-status.processing { background: #fff3e0; }
.order-status.completed { background: #e8f5e9; }
.order-status.cancelled { background: #ffebee; }

.order-date {
  color: #666;
  font-size: 14px;
  margin-bottom: 16px;
}

.order-items {
  margin-bottom: 16px;
}

.order-item {
  display: flex;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.item-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}

.item-details {
  flex: 1;
}

.item-name {
  font-weight: 500;
  margin-bottom: 4px;
}

.item-variant {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.order-total {
  font-weight: bold;
  text-align: right;
  margin-top: 12px;
}
</style> 