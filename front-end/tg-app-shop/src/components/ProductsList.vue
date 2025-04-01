<template>
  <div class="product-list justify-content-center">
    <div class="row ">
      <div class="col-sm-6 col-lg-4 p-2" v-for="product in products" :key="product.id">
        <router-link :to="`/product/${product.id}`" class="product-card product-card-link">
          <div class="product-card-image">
            <img :src="product.image" alt="Изображение продукта" class="product-image" />
          </div>
          <h2 class="product-name">{{ product.name }}</h2>
          
          <div class="item-price-container">
            <p v-if="product.productOldPrice > 0" class="product-price old-price">{{ product.productOldPrice.toLocaleString() }} ₽</p>
            <p class="product-price">{{ product.productPrice.toLocaleString() }} ₽</p>
          </div>
        </router-link>
          <div class="button-container">
            <span @click="toggleLike(product)" :class="['icon', 'like-icon', { 'red-icon': product.like }]">
              <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.09.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/>
              </svg>       
            </span>
            <router-link :to="`/product/${product.id}`" class="product-card-link">
              <span  class="icon cart-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-cart" viewBox="0 0 16 16">
                  <path d="M0 1.5A.5.5 0 0 1 .5 1H2a.5.5 0 0 1 .485.379L2.89 3H14.5a.5.5 0 0 1 .491.592l-1.5 8A.5.5 0 0 1 13 12H4a.5.5 0 0 1-.491-.408L2.01 3.607 1.61 2H.5a.5.5 0 0 1-.5-.5M3.102 4l1.313 7h8.17l1.313-7zM5 12a2 2 0 1 0 0 4 2 2 0 0 0 0-4m7 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4m-7 1a1 1 0 1 1 0 2 1 1 0 0 1 0-2m7 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2"/>
                </svg>
              </span>
            </router-link>
          </div>
      </div>
    </div>
  </div>
</template>

<script>
import API_BASE_URL from '../config';

export default {
  props: {
    products: {
      type: Array,
      default: [
        {
          id: 1,
          name: 'Product 1',
          price: 100,
          image: 'https://via.placeholder.com/150',
          like: false
        }
      ],
      required: true
    }
  },
  methods: {
    toggleLike(product) {
      product.like = !product.like;
      
      const tgUserId = this.getUserId(); 
      fetch(`${API_BASE_URL}/like`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ productId: product.id, tgUserId }),
      })
      .then(response => response.json())
      .then(data => {
        console.log('Успех:', data);
        product.like = !product.like;
      })
      .catch((error) => {
        console.error('Ошибка:', error);
      });
    },
   
    
  }
}
</script>

<style>
.product-card-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
  border-radius: 10px;
}

.old-price {
  text-decoration: line-through;
  margin-right: 10px;
}
.product-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}
.product-card-link {
  text-decoration: none; /* Убираем подчеркивание */
  color: inherit; /* Наследуем цвет текста */
}
.product-card {
  flex: 0 0 48%; /* Два товара на строку */
  margin-bottom: 20px;
  border: none; /* Убираем рамки */
}

.product-image {
  width: 100%; /* Большое изображение без рамок */
  height: auto;
}

.product-name {
  color: black; /* Или white, в зависимости от фона */
  font-weight: 300; /* Тонкий шрифт */
}

.product-price {
  font-weight: 300; /* Тонкий шрифт */
}

.button-container {
  display: flex;
  justify-content: space-between; /* Размещаем иконки по краям */
  margin-top: 1px;
}

.icon {
  cursor: pointer; /* Указатель при наведении */
  font-size: 24px; /* Размер иконок */
}

.red-icon {
  color: red; /* Задаем красный цвет */
}
</style>
