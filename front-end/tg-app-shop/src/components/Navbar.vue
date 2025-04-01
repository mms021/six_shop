<template>
  <!-- Верхняя шапка -->
  <nav class="navbar bg-light p-1"> 
    <div class="menu-container p-3">
      <router-link to="/cart" class="navbar-link btn btn-outline-secondary ml-auto">
        <i class="bi bi-cart"></i>
      </router-link>
    </div>

    <div class="navbar-brand" style="margin-left: 13%;">
      <router-link to="/" class="navbar-brand">
        <img src="@/assets/logo.png" alt="logo" class="logo" />
      </router-link>
    </div>

    <div class="menu-container p-3">
      <button @click="isMenuOpen = !isMenuOpen" class="btn btn-outline-secondary">
        <i class="bi" :class="{'bi-chevron-up': isMenuOpen, 'bi-chevron-down': !isMenuOpen}"></i>
      </button>
    </div>   
  </nav>

  <!-- Выпадающее меню с поиском и категориями -->
  <nav class="navbar navbar-expand-lg bg-white" v-if="isMenuOpen">
    <div class="container-fluid">
      <div class="row w-100">
        <div class="col">
          <div class="search-bar-container">
            <SearchBar />
          </div>
        </div>
        <div class="col-2" >
          <router-link 
            to="/admin-page" 
            @click="closeMenu" 
            class="btn btn-outline-secondary"
          >
            Admin
          </router-link>
        </div>
      </div>

      <!-- Список категорий -->
      <div class="categories-list">
        <div class="nav-grid">
          <li class="nav-item">
            <router-link 
              to="/favorites" 
              class="nav-link d-flex align-items-center"
              @click="closeMenu"
            >
              <i class="bi bi-heart me-2"></i>
              Понравившиеся товары
            </router-link>
          </li>
          
          <li class="nav-item">
            <router-link 
              to="/cart" 
              class="nav-link d-flex align-items-center"
              @click="closeMenu"
            >
              <i class="bi bi-cart me-2"></i>
              Корзина
            </router-link>
          </li>
          
          <li class="nav-item">
            <router-link 
              to="/concierge" 
              class="nav-link d-flex align-items-center"
              @click="closeMenu"
            >
              <i class="bi bi-person-circle me-2"></i>
              Консьерж сервис
            </router-link>
          </li>
          
          <li class="nav-item">
            <router-link 
              to="/order-history" 
              class="nav-link d-flex align-items-center"
              @click="closeMenu"
            >
              <i class="bi bi-clock-history me-2"></i>
              История покупок
            </router-link>
          </li>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref, onMounted } from 'vue';
import { API_BASE_URL } from '../config';
import SearchBar from '@/components/SearchBar.vue';
import axios from 'axios';

export default {
  name: 'Navbar',
  components: {
    SearchBar
  },
  setup() {
    const categories = ref([]);
    const isMenuOpen = ref(false);
    const isAdmin = ref(false);
    
    const closeMenu = () => {
      isMenuOpen.value = false;
    };
    
    const fetchCategories = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/categories`);
        categories.value = response.data;
      } catch (error) {
        console.error('Ошибка при получении категорий:', error);
      }
    };

    const checkAdminStatus = async () => {
      try {
        // Получаем данные пользователя из Telegram WebApp
        const initDataUnsafe = window.Telegram.WebApp.initDataUnsafe;
        if (!initDataUnsafe.user) return;

        const response = await axios.get(`${API_BASE_URL}/api/user/status`, {
          headers: {
            'Telegram-Data': window.Telegram.WebApp.initData
          }
        });
        
        isAdmin.value = response.data.is_admin;
      } catch (error) {
        console.error('Ошибка при проверке статуса администратора:', error);
        isAdmin.value = false;
      }
    };

    onMounted(() => {
      fetchCategories();
      checkAdminStatus();
    });

    return {
      categories,
      isMenuOpen,
      isAdmin,
      closeMenu
    }
  }
}
</script>

<style scoped>
/* Стили для верхней шапки */
.logo {
  width: 80px;
  height: 80px;
}

.logo:hover {
  transform: rotate(90deg);
  transition: transform 0.5s ease;
}

.navbar-link {
  margin-left: 1rem;
  text-decoration: none;
  font-weight: 500;
  font-size: 1.1rem;
  color: #6c757d;
  border-color: #e9ecef;
  background-color: transparent;
}

.navbar-link:hover {
  background-color: #f8f9fa;
  color: #495057;
  border-color: #dee2e6;
}

.search-bar-container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  padding: 0 15px;
}

/* Стили для списка категорий */
.categories-list {
  width: 100%;
  padding: 1.5rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin-top: 1rem;
  padding-left: 0;
}

.nav-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  width: 100%;
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  width: 100%;
  margin: 0;
  list-style: none;
}

.nav-link {
  padding: 10px;
  color: var(--tg-theme-text-color);
  text-decoration: none;
  transition: background-color 0.3s;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  border-radius: 8px;
  background: var(--tg-theme-bg-color);
}

.nav-link:hover {
  background-color: var(--tg-theme-secondary-bg-color);
}

.nav-link i {
  font-size: 1.2em;
  margin-right: 8px;
}

/* Стиль для пункта избранного */
.nav-link.d-flex {
  color: #6c757d;
  font-weight: 500;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.nav-link.d-flex:hover {
  color: #495057;
  background-color: #f8f9fa;
  transform: translateX(5px);
}

/* Анимация для активных ссылок */
.router-link-active {
  color: #495057 !important;
  
  
}

.subcategory-link.router-link-active {
  border-left-color: #495057;
}

/* Кнопка меню */
.btn-outline-secondary {
  color: #6c757d;
  border-color: #e9ecef;
  background-color: transparent;
}

.btn-outline-secondary:hover {
  background-color: #f8f9fa;
  color: #495057;
  border-color: #dee2e6;
}

/* Медиа-запросы */
@media (max-width: 991.98px) {
  .search-container {
    max-width: 100%;
  }
  
  .nav-item {
    padding: 0.3rem 0;
  }
  
  .categories-list {
    padding: 1rem;
  }
  
  .subcategory-item {
    margin-left: 1.2rem;
  }
}
</style>