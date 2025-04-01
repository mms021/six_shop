<template>
  <div class="products">
    <h1 class="press-start text-center" >{{ productName }}</h1>
    <div class="product-detail">
      <swiper 
      class="swiper"
      :modules="modules"
      :space-between="30"
      :slides-per-view="1.2"
      :centered-slides="true"
      :pagination="{ clickable: true }"
      >
        <swiper-slide v-for="(image, index) in productImages" :key="index">
          <div class="image-container no-image">
              <img :src="getFullImageUrl(image.image_url)" class="d-block w-100 " alt="Product Image"  />
          </div>
        </swiper-slide>

      </swiper>
      <hr class="my-2">
      <div class="row">
        <div class="col-12">
          <h2 class="press-start p-1">О товаре</h2>
          <p>{{ productDescription }}</p>
        </div>
      </div>
      <div class="">
        <div class="row">
          <div class="col-5 product-price-container">
            <p>Цена: </p>
            <p v-if="productOldPrice > 0" class="old-price"> {{ productOldPrice }} ₽.</p>
            <p> {{ productPrice.toLocaleString() }} ₽</p>
          </div>
          <div class="col-7" v-if="productsVariants.length > 0">
            <select v-model="selectedVariant" class="form-select" aria-label="Выберите размер">
              <option value="0" disabled>{{ defaultVariantText }}</option>
              <option v-for="variant in productsVariants" :key="variant.variant_id" :value="variant.variant_id">
                {{ variant.variant_name }}
              </option>
            </select>
          </div>
        </div>
      </div>
     
      
      <hr class="my-2">
      <div class="button-container">
        <button @click="toggleLike" class="btn btn-default" style="border-color: #FFFAFA; ">
          <svg v-if="isLiked" xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16" style="color: red;" > 
                <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.09.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/>
            </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-bag-heart" viewBox="0 0 16 16">
            <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.09.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/>  
          </svg>
        </button>
        <button @click="addToCart" class="btn btn-outline-secondary" >
          <span class="px-2">Добавить в корзину</span>
          <svg v-if="isInCart" xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-bag-check" viewBox="0 0 16 16" style="color: green;">
            <path fill-rule="evenodd" d="M10.854 8.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 0 1 .708-.708L7.5 10.793l2.646-2.647a.5.5 0 0 1 .708 0"/>
            <path d="M8 1a2.5 2.5 0 0 1 2.5 2.5V4h-5v-.5A2.5 2.5 0 0 1 8 1m3.5 3v-.5a3.5 3.5 0 1 0-7 0V4H1v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V4zM2 5h12v9a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1z"/>
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-bag" viewBox="0 0 16 16">
            <path d="M8 1a2.5 2.5 0 0 1 2.5 2.5V4h-5v-.5A2.5 2.5 0 0 1 8 1m3.5 3v-.5a3.5 3.5 0 1 0-7 0V4H1v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V4zM2 5h12v9a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1z"/>
          </svg>
        </button>
      </div>
      <hr class="my-3">

      <div class="row">
        <div class="col-6">
          <div class="list-group">
            <router-link to="/category-products" class="list-group-item list-group-item-action d-flex " aria-current="true">
              <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class=" rounded-circle flex-shrink-0 p-1" viewBox="0 0 16 16">
                <path d="M3 2v4.586l7 7L14.586 9l-7-7H3zM2 2a1 1 0 0 1 1-1h4.586a1 1 0 0 1 .707.293l7 7a1 1 0 0 1 0 1.414l-4.586 4.586a1 1 0 0 1-1.414 0l-7-7A1 1 0 0 1 2 6.586V2z"/>
                <path d="M5.5 5a.5.5 0 1 1 0-1 .5.5 0 0 1 0 1zm0 1a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3zM1 7.086a1 1 0 0 0 .293.707L8.75 15.25l-.043.043a1 1 0 0 1-1.414 0l-7-7A1 1 0 0 1 0 7.586V3a1 1 0 0 1 1-1v5.086z"/>
              </svg>
              <div class="d-flex gap-2  w-100 justify-content-between">
                <div>
                  <h6 class="mb-0 press-start">{{ productCategory }}</h6>
                  <p class="mb-0 opacity-75">Категория</p>
                </div>
              </div>
            </router-link>
          </div>
        </div>
        <div class="col-6">
          <div class="list-group">
            <router-link to="/category-products" class="list-group-item list-group-item-action d-flex " aria-current="true">
              <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="rounded-circle flex-shrink-0 p-1" viewBox="0 0 16 16">
                <path d="M3.1.7a.5.5 0 0 1 .4-.2h9a.5.5 0 0 1 .4.2l2.976 3.974c.149.185.156.45.01.644L8.4 15.3a.5.5 0 0 1-.8 0L.1 5.3a.5.5 0 0 1 0-.6zm11.386 3.785-1.806-2.41-.776 2.413zm-3.633.004.961-2.989H4.186l.963 2.995zM5.47 5.495 8 13.366l2.532-7.876zm-1.371-.999-.78-2.422-1.818 2.425zM1.499 5.5l5.113 6.817-2.192-6.82zm7.889 6.817 5.123-6.83-2.928.002z"/>
              </svg>
              <div class="d-flex gap-2  w-100 justify-content-between">
                <div>
                  <h6 class="mb-0 press-start">{{ productBrand }}</h6>
                  <p class="mb-0 opacity-75">Бренд</p>
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </div>

      <h2 class="text-center press-start p-1">Возможно, вам понравится</h2>
      <ProductsList :products="relatedProducts" />
    </div>
  </div>
</template>





<script>
 
import { Pagination, EffectCoverflow } from 'swiper'
import { Swiper, SwiperSlide } from 'swiper/vue'
import 'swiper/css'
import 'swiper/css/pagination'
import 'swiper/css/effect-coverflow'
import { API_BASE_URL, STATIC_URL } from '../config.js';
import ProductsList from '@/components/ProductsList.vue';
import { useAuth } from '@/composables/useAuth'
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

export default {
  name: 'ProductDetailView',
  components: {
    Swiper,
    SwiperSlide,
    ProductsList
  },
  setup() {
      return {
        modules: [Pagination, EffectCoverflow]
      }
    },
  data() {
    return {
      productId: 1, 
      productName: 'Название продукта',
      productDescription: 'Описание продукта...',
      productPrice: 120000,
      productOldPrice: 16000, 
      productCategory: 'Категория продукта',
      productBrand: 'Бренд продукта',
      productImages: [{ image_url: 'url_изображения_1' }, { image_url: 'url_изображения_2' }],
      productsVariants: [
                    { variant_id: 1, variant_name: 'Вариант 1', }, 
                    { variant_id: 2, variant_name: 'Вариант 2', }], 
      isLiked: false,
      isInCart: false, 
      selectedVariant: null, 
      swiperOptions: {
        pagination: {
          el: '.swiper-pagination'
        },
      },
      defaultVariantText: 'Выберите размер', 
      relatedProducts: [
        { id: 1, name: 'Продукт 1', productPrice: 10000, productOldPrice: 12.00, image: 'url_к_изображению_1' },
        { id: 2, name: 'Продукт 2', productPrice: 2000, productOldPrice: 0.00, image: 'url_к_изображению_2' },
        { id: 3, name: 'Продукт 3', productPrice: 300, productOldPrice: 32.00, image: 'url_к_изображению_3' },
      ],
    }
    
  },
  created() {
    // Устанавливаем выбранный вариант по умолчанию на null
    this.selectedVariant = 0;
  },
  methods: {
    async toggleLike() {
      try {
        const { checkAuth } = useAuth()
        const userData = await checkAuth()
        
        const response = await fetch(`${API_BASE_URL}/api/like`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Telegram-Data': useWebApp().initData
          },
          body: JSON.stringify({ 
            userId: userData.tg_id,
            productId: this.productId
          })
        })

        const result = await response.json()
        if (result.success) {
          this.isLiked = result.isLiked
        }
      } catch (error) {
        console.error('Ошибка:', error)
      }
    },
    async addToCart() {
      try {
        const { checkAuth } = useAuth()
        const userData = await checkAuth()

        const response = await fetch(`${API_BASE_URL}/api/cart`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Telegram-Data': useWebApp().initData
          },
          body: JSON.stringify({ 
            productId: this.productId,
            userId: userData.tg_id,
            variantId: this.selectedVariant
          })
        })

        if (!response.ok) {
          throw new Error('Ошибка при добавлении в корзину')
        }

        this.isInCart = true
      } catch (error) {
        console.error('Ошибка:', error)
        // Можно добавить уведомление пользователю
      }
    },
    getFullImageUrl(path) {
      if (!path) return '';
      // Если путь уже содержит полный URL, возвращаем его как есть
      if (path.startsWith('http')) return path;
      // Иначе добавляем базовый URL для статических файлов
      return `${STATIC_URL}${path}`;
    }
  }
}
</script>

<style>
.rounded-circle {
  border-radius: 50%;
  border: 1px solid black;
  margin-right: 10px;
}

.product-price-container {
  display: flex;
  align-items: left;
}

.image-container {
  max-height: 500px;
  height: 200px;
  overflow: hidden;
}

.image-container :is(img) {
  width: 100%;
  height: auto;
  object-fit: cover;
}

.variant-select {
  width: 100%;
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f9f9f9;
  cursor: pointer;
}
.coverflow-example {
    @include swiper-wrapper($height: 380px);
    position: relative;
  }

  .swiper {
    height: 100%;
    width: 100%;
    padding-top: 20px;
    padding-bottom: 50px;

    .slide {
      width: 300px;
      height: 300px;

      :is(img) {
        display: block;
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
    }
  }

.no-image {
  background-color: #D3D3D3; /* Серый фон для отсутствующего изображения */
  display: block;
  border-radius: 10px;
}
</style>


        