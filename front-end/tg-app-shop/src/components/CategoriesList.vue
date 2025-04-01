<template>
  <div class="categories-list-view">
    <swiper 
    class="swiper"
    :modules="modules"
    :space-between="20"
    :centered-slides="true"
    :navigation="true"
    :pagination="{
      clickable: true
    }"
    :autoplay="{
      delay: 2500,
      disableOnInteraction: false
    }"
    :breakpoints="{
      // когда ширина окна >= 320px
      320: {
        slidesPerView: 1.2,
        spaceBetween: 10
      },
      // когда ширина окна >= 480px
      480: {
        slidesPerView: 2,
        spaceBetween: 15
      },
      // когда ширина окна >= 768px
      768: {
        slidesPerView: 3,
        spaceBetween: 20
      }
    }"
    >
      <swiper-slide class="slide" v-for="category in categories" :key="category.id">
        <div class="category-card">
          <a :href="category.link" class="category-link">
            <div class="image-container">
              <img :src="getFullImageUrl(category.image)" class="category-image" :alt="category.name">
              <div class="category-overlay">
                <h5 class="category-title">{{ category.name }}</h5>
              </div>
            </div>
          </a>
        </div>
      </swiper-slide>
    </swiper>
  </div>
</template>

<script>
import { Pagination, Navigation, Autoplay } from 'swiper'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { API_BASE_URL, STATIC_URL } from '../config';

// Import Swiper styles
import 'swiper/css'
import 'swiper/css/pagination'
import 'swiper/css/navigation'

export default {
  components: {
    Swiper,
    SwiperSlide
  },
  props: {
    categories: {
      type: Array,
      required: true
    }
  },
  setup() {
    const getFullImageUrl = (path) => {
      if (!path) return '';
      // Если путь уже содержит полный URL, возвращаем его как есть
      if (path.startsWith('http')) return path;
      // Иначе добавляем базовый URL для статических файлов
      return `${STATIC_URL}${path}`;
    }

    return {
      modules: [Pagination, Navigation, Autoplay],
      getFullImageUrl
    }
  },
  methods: {
    onSlideChange(swiper) {
      console.log('Слайд изменен на:', swiper.activeIndex);
      // Здесь можно добавить дополнительную логику при изменении слайда
    }
  },
}
</script>

<style scoped>
.swiper {
  width: 100%;
  height: 100%;
  padding-top: 10px;
  padding-bottom: 30px;
}

.category-card {
  width: 100%;
  height: 240px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.category-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.category-link {
  text-decoration: none;
  color: inherit;
  display: block;
  height: 100%;
}

.image-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.category-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.category-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.7), transparent);
  padding: 15px;
  display: flex;
  align-items: flex-end;
  height: 50%;
}

.category-title {
  color: white;
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
}

/* Стили для пагинации */
:deep(.swiper-pagination-bullet) {
  background-color: #333;
  opacity: 0.5;
}

:deep(.swiper-pagination-bullet-active) {
  background-color: #000;
  opacity: 1;
}

/* Стили для навигационных кнопок */
:deep(.swiper-button-next),
:deep(.swiper-button-prev) {
  color: #333;
  background-color: rgba(255, 255, 255, 0.7);
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

:deep(.swiper-button-next:after),
:deep(.swiper-button-prev:after) {
  font-size: 14px;
  font-weight: bold;
}
</style>
