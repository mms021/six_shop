<script setup>
import { STATIC_URL } from '../config';

const getFullImageUrl = (path) => {
  if (!path) return '';
  // Если путь уже содержит полный URL, возвращаем его как есть
  if (path.startsWith('http')) return path;
  // Иначе добавляем базовый URL для статических файлов
  return `${STATIC_URL}${path}`;
}
</script>

<template>
  <div class="product-card">
    <img :src="getFullImageUrl(product.image)" :alt="product.name" class="product-image" />
    <!-- ... -->
  </div>
</template> 