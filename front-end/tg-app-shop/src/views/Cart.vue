<template>
  <div class="cart">
    <div class="cart-header">
      <h1>Корзина</h1>
      <button class="history-btn" @click="goToHistory">
        История заказов
      </button>
    </div>
    <hr class="p-1">
    <div v-if="cartItems.length === 0" class="empty-cart-message">Ваша корзина пуста.</div>
    <div v-else>
      <div class="cart-item cart-item-row" v-for="item in cartItems" :key="item.id" :class="{ 'fade-out': item.removing }">
        <div class="row">
            <div class="col-3" >
              <img :src="getFullImageUrl(item.image)" alt="Изображение товара" class="item-image" />
            </div>
            <div class="col-7">
              <h2>{{ item.name }}</h2>
              <p>{{ item.productDescription }}</p>

                <div class="item-price-container">
                  <p v-if="item.productOldPrice > 0" class="item-price old-price">{{ item.productOldPrice }} ₽</p>
     
                  <p class="item-price"> {{ item.productPrice.toLocaleString() }} ₽</p>
                </div>
            </div>
            
            <div class="col-2">
              <button @click="removeFromCart(item.id)" class="btn btn-outline-secondary" style="border-color: #FFFAFA; ">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                  <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                  <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                </svg>
              </button>
            </div>
        </div>
      </div>
      <hr class="p-1">
      <div class="cart-total" style="display: flex; justify-content: space-between; align-items: center;">
        <p style="font-weight: bold;align-items: center;">Итого: {{ totalPrice }} ₽</p>
        <button 
          v-if="!showUserForm" 
          class="checkout-btn" 
          @click="startCheckout" 
          :disabled="!cartItems.length"
        >
          Оформить заказ
        </button>
      </div>
      <hr class="p-1">
      <div v-if="showUserForm" class="user-form">
        <h2>Данные для доставки</h2>
        <form @submit.prevent="submitOrder">
          <div class="form-group">
            <label for="name">Имя*</label>
            <input 
              id="name" 
              v-model="userData.name" 
              type="text" 
              required
              placeholder="Ваше имя"
            >
          </div>
          
          <div class="form-group">
            <label for="phone">Телефон*</label>
            <input 
              id="phone" 
              v-model="userData.phone" 
              type="tel"
              required
              placeholder="+7 (___) ___-__-__"
            >
          </div>
          
          <div class="form-group">
            <label for="email">Email</label>
            <input 
              id="email" 
              v-model="userData.email" 
              type="email"
              placeholder="example@mail.com"
            >
          </div>
          
          <div class="form-group">
            <label for="address">Адрес доставки*</label>
            <textarea 
              id="address" 
              v-model="userData.address" 
              required
              placeholder="Укажите адрес доставки"
            ></textarea>
          </div>
          
          <div class="form-group">
            <label for="comment">Комментарий к заказу</label>
            <textarea 
              id="comment" 
              v-model="userData.comment"
              placeholder="Дополнительная информация к заказу"
            ></textarea>
          </div>
          
          <div class="form-group checkbox">
            <input 
              id="privacy" 
              v-model="privacyAccepted" 
              type="checkbox"
              required
            >
            <label for="privacy">
              Я согласен с <a href="/privacy" target="_blank">политикой конфиденциальности</a>
            </label>
          </div>
          
          <div class="form-buttons">
            <button type="button" class="back-btn" @click="showUserForm = false">
              Назад
            </button>
            <button 
              type="submit" 
              class="submit-btn" 
              :disabled="!privacyAccepted"
            >
              Подтвердить заказ
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { API_BASE_URL, STATIC_URL } from '../config';
import axios from 'axios';
import { useAuth } from '../composables/useAuth';

const { user } = useAuth();
const cartItems = ref([]);
const loading = ref(true);
const error = ref(null);
const showUserForm = ref(false);
const privacyAccepted = ref(false);
const userData = ref({
  name: '',
  phone: '',
  email: '',
  address: '',
  comment: ''
});

const fetchCartItems = async () => {
  try {
    loading.value = true;
    const response = await axios.get(`${API_BASE_URL}/api/cart/items?user_id=${user.value.id}`);
    cartItems.value = response.data;
  } catch (err) {
    error.value = 'Ошибка при загрузке корзины';
    console.error('Ошибка:', err);
  } finally {
    loading.value = false;
  }
};

const removeFromCart = async (id) => {
  try {
    const item = cartItems.value.find(item => item.id === id);
    if (item) {
      item.removing = true;
      await axios.delete(`${API_BASE_URL}/api/cart/items/${id}`, {
        data: { user_id: user.value.id }
      });
      setTimeout(() => {
        cartItems.value = cartItems.value.filter(item => item.id !== id);
      }, 300);
    }
  } catch (err) {
    console.error('Ошибка при удалении:', err);
  }
};

const totalPrice = computed(() => {
  return cartItems.value.reduce((total, item) => total + item.productPrice, 0);
});

const checkout = async () => {
  // Здесь будет логика оформления заказа
  console.log('Оформление заказа...');
};

const goToHistory = () => {
  // Реализация перехода к истории заказов
  console.log('Переход к истории заказов');
};

const startCheckout = () => {
  showUserForm.value = true;
};

const submitOrder = async () => {
  try {
    // Обновляем статус заказа и данные пользователя
    const response = await axios.post(`${API_BASE_URL}/api/orders/checkout`, {
      cartId: cartItems.value.map(item => item.id),
      userData: userData.value
    });
    
    if (response.data.success) {
      // Переход к успешному оформлению заказа
      console.log('Заказ успешно оформлен');
    }
  } catch (error) {
    console.error('Ошибка при оформлении заказа:', error);
  }
};

const getFullImageUrl = (path) => {
  if (!path) return '';
  if (path.startsWith('http')) return path;
  return `${STATIC_URL}${path}`;
}

onMounted(() => {
  fetchCartItems();
});
</script>

<style>
.cart {
  padding: 20px;
}
.cart-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}
.cart-item {
  margin: 10px 0;
  transition: opacity 0.5s ease; /* Увеличено время для плавного перехода */
}
.fade-out {
  opacity: 0; /* Прозрачность для анимации удаления */
}
.item-price {
  font-size: 16px;
  font-weight: bold;
}
.old-price {
  text-decoration: line-through;
  margin-right: 10px;
}
.item-price-container {
  display: flex;
  align-items: end;
}
.item-image {
 
  min-width: 90%; 
  min-height: 90%;
  object-fit: cover;
  border-radius: 50%;
  border: 1px solid gray;
}
.empty-cart-message {
  text-align: center;
  font-size: 20px;

  padding-top: 40px; /* Центрирование текста */
}
.cart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.history-btn {
  padding: 8px 16px;
  background: #f0f0f0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.user-form {
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.form-group {
  margin-bottom: 16px;
}
.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}
.form-group input,
.form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.form-group textarea {
  min-height: 80px;
}
.checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
}
.checkbox input {
  width: auto;
}
.form-buttons {
  display: flex;
  gap: 16px;
  margin-top: 24px;
}
.back-btn,
.submit-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.back-btn {
  background: #f0f0f0;
}
.submit-btn {
  background: var(--tg-theme-button-color);
  color: var(--tg-theme-button-text-color);
}
.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style> 