<template>
   <div>
      <Navbar /> 
      <div class="container test p-2">
         <router-view />
      </div>
      <Footer />
   </div>
</template>


<script setup>
import { ref, onMounted } from 'vue';
import { defineComponent } from 'vue';
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import ProductList from '@/components/ProductsList.vue';
import CategoriesList from '@/components/CategoriesList.vue';
import 'bootstrap/dist/css/bootstrap.min.css';
import { API_BASE_URL } from './config';
import { useAuth } from './composables/useAuth';

const isLoading = ref(true);
const fadeOut = ref(false);
const userInfo = ref(null);
const error = ref(null);
const userType = ref(null);

const { user, fetchUserInfo } = useAuth();

onMounted(async () => {
  setTimeout(() => {
    fadeOut.value = true; 
    setTimeout(() => {
      isLoading.value = false; 
    }, 30); 
  }, 1); 
  
  if (window.Telegram?.WebApp) {
    const webApp = window.Telegram.WebApp;
    if (webApp.initDataUnsafe) {
      const user = webApp.initDataUnsafe.user;
      userType.value = webApp.initDataUnsafe.user?.type;
      console.log('User:', user);
      console.log('User type:', userType.value);
    }
  }
  
  await fetchUserInfo();
});

const routes = [
  { path: '/', component: ProductList },
];  

const app = defineComponent({
  name: 'App',
  components: {
    ProductList,
    CategoriesList,
    Navbar,
    Footer,
  },
  data() {
    return {
      userInfo,
      TOKEN,
      error,
    };
  },
});
</script>


<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap'); /* Импорт шрифтов */

@import url('https://fonts.googleapis.com/css2?family=Jura:wght@300;400;500;600;700&display=swap'); /* Импорт шрифта Jura */
body {
  font-family: 'Roboto', sans-serif;
}

.large-logo {
  width: 100%; /* Установите ширину логотипа */
  max-width: 400px; /* Максимальная ширина логотипа */
  margin: auto; /* Центрирование логотипа */
  display: block; /* Блочный элемент для центрирования */
  transition: opacity 1ms ease; /* Увеличено время перехода для более плавного растворения */
  opacity: 1; /* Начальная непрозрачность */
}

.large-logo[style*="opacity: 0"] {
  opacity: 0; /* Непрозрачность при растворении */
}

.test  {
  min-height: 70vh; /* Установите высоту на 100% высоты окна */
}

@media (max-width: 768px) {
  .container {
    padding: 1rem; /* Уменьшите отступы для меньших экранов */
    
  }
}

@media (min-width: 769px) {
  .container {
    padding: 2rem; /* Увеличьте отступы для больших экранов */
  }
}

.press-start {
  font-family: 'Jura', cursive; 
}
.old-price {
  text-decoration: line-through;
  margin-right: 10px;
}
</style>

