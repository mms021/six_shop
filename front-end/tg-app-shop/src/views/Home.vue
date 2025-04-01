<template>
  <div class="home">
    <h2 class="text-center press-start p-1"> Брендовые вещи со всего мира, каждый день ровно в 18:00</h2>
    <CategoriesList :categories="categoriesList" />
    
    <h2 class="text-center press-start p-1" >Новинки и лучшие предложения</h2>
    <hr class="my-3">
    <ProductsList :products="bestProducts" />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { API_BASE_URL } from '../config';
import CategoriesList from '@/components/CategoriesList.vue';
import ProductsList from '@/components/ProductsList.vue';
import axios from 'axios';

export default {
  components: {
    CategoriesList,
    ProductsList
  },
  data() {
    return {
      categoriesList: [],
      bestProducts: []
    }
  },
  async mounted() {
    await Promise.all([
      this.fetchCategories(),
      this.fetchBestProducts()
    ]);
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/categories`);
        this.categoriesList = response.data.map(category => ({
          id: category.id,
          name: category.name,
          image: category.image || 'https://via.placeholder.com/150',
          link: `/category/${category.id}`
        }));
        console.log('Categories loaded:', this.categoriesList);
      } catch (error) {
        console.error('Ошибка при получении категорий:', error);
      }
    },
    async fetchBestProducts() {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/products/best`, {
          params: {
            user_id: user.value?.id || ''
          }
        });
        this.bestProducts = response.data;
        console.log('Products loaded:', this.bestProducts);
      } catch (error) {
        console.error('Ошибка при получении продуктов:', error);
      }
    }
  }
};
</script>

<style>

</style> 