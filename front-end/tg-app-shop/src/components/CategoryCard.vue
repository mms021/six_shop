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
  <div class="category-card">
    <img :src="getFullImageUrl(category.image_url)" :alt="category.name" class="category-image" />
    <div class="category-name">{{ category.name }}</div>
  </div>
</template> 