<template>
  <div class="admin-products">
    <h2 class="press-start p-1">{{ isEditing ? 'Редактировать товар' : 'Создать товар' }}</h2>

    <form @submit.prevent="handleSubmit" class="product-form p-3">
      <!-- Основная информация -->
      <div class="row">
        <div class="col-md-6 mb-3">
          <label class="form-label">Название товара</label>
          <input 
            v-model="form.name" 
            type="text" 
            class="form-control"
            required
          >
        </div>

        <div class="col-md-6 mb-3">
          <label class="form-label">Категория</label>
          <select v-model="form.category_id" class="form-select" required>
            <option value="">Выберите категорию</option>
            <option 
              v-for="category in categories" 
              :key="category.id"
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>
        </div>

        <div class="col-md-4 mb-3">
          <label class="form-label">Цена</label>
          <input 
            v-model.number="form.price" 
            type="number" 
            class="form-control"
            required
            min="0"
            step="0.01"
          >
        </div>

        <div class="col-md-4 mb-3">
          <label class="form-label">Старая цена</label>
          <input 
            v-model.number="form.old_price" 
            type="number" 
            class="form-control"
            min="0"
            step="0.01"
          >
        </div>

        <div class="col-md-4 mb-3">
          <label class="form-label">Бренд</label>
          <input 
            v-model="form.brand" 
            type="text" 
            class="form-control"
          >
        </div>
      </div>

      <!-- Описание -->
      <div class="mb-3">
        <label class="form-label">Описание</label>
        <textarea 
          v-model="form.description" 
          class="form-control"
          rows="4"
          required
        ></textarea>
      </div>

      <!-- Варианты -->
      <div class="mb-3">
        <label class="form-label">Варианты (размеры)</label>
        <div class="variants-list">
          <div 
            v-for="(variant, index) in form.variants" 
            :key="index"
            class="variant-item d-flex gap-2 mb-2"
          >
            <input 
              v-model="variant.name" 
              type="text" 
              class="form-control"
              placeholder="Название варианта"
            >
            <button 
              type="button" 
              class="btn btn-outline-danger"
              @click="removeVariant(index)"
            >
              Удалить
            </button>
          </div>
        </div>
        <button 
          type="button" 
          class="btn btn-outline-primary mt-2"
          @click="addVariant"
        >
          Добавить вариант
        </button>
      </div>

      <!-- Изображения -->
      <div class="mb-3">
        <label class="form-label">Изображения</label>
        <input 
          type="file" 
          class="form-control mb-2"
          @change="handleImagesChange"
          multiple
          accept="image/*"
        >
        <div class="images-preview row">
          <div 
            v-for="(image, index) in form.images" 
            :key="index"
            class="col-4 col-md-3 mb-3"
          >
            <div class="image-preview-item">
              <img :src="image.url" :alt="`Preview ${index + 1}`">
              <div class="image-actions">
                <button 
                  type="button" 
                  class="btn btn-sm btn-primary"
                  @click="setMainImage(index)"
                  :disabled="form.main_image_index === index"
                >
                  {{ form.main_image_index === index ? 'Главное' : 'Сделать главным' }}
                </button>
                <button 
                  type="button" 
                  class="btn btn-sm btn-danger"
                  @click="removeImage(index)"
                >
                  Удалить
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Кнопки управления -->
      <div class="d-flex gap-2">
        <button type="submit" class="btn btn-primary">
          {{ isEditing ? 'Обновить' : 'Создать' }}
        </button>
        <button 
          v-if="isEditing" 
          type="button" 
          class="btn btn-secondary"
          @click="cancelEdit"
        >
          Отмена
        </button>
      </div>
    </form>

    <!-- Список товаров -->
    <div class="products-list mt-4">
      <h3>Список товаров</h3>
      
      <!-- Фильтры -->
      <div class="filters row mb-3">
        <div class="col-md-4">
          <input 
            v-model="filters.search" 
            type="text" 
            class="form-control"
            placeholder="Поиск по названию..."
            @input="handleSearch"
          >
        </div>
        <div class="col-md-4">
          <select 
            v-model="filters.category" 
            class="form-select"
            @change="fetchProducts"
          >
            <option :value="null">Все категории</option>
            <option 
              v-for="category in categories" 
              :key="category.id"
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>
        </div>
      </div>

      <!-- Таблица товаров -->
      <div class="table-responsive">
        <table class="table">
          <thead>
            <tr>
              <th>Изображение</th>
              <th>Название</th>
              <th>Категория</th>
              <th>Цена</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in products" :key="product.id">
              <td>
                <img 
                  :src="product.image" 
                  :alt="product.name"
                  class="product-thumbnail"
                >
              </td>
              <td>{{ product.name }}</td>
              <td>{{ product.category }}</td>
              <td>{{ product.price }} ₽</td>
              <td>
                <div class="btn-group">
                  <button 
                    class="btn btn-sm btn-outline-primary"
                    @click="editProduct(product)"
                  >
                    Редактировать
                  </button>
                  <button 
                    class="btn btn-sm btn-outline-danger"
                    @click="deleteProduct(product.id)"
                  >
                    Удалить
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Пагинация -->
      <nav v-if="totalPages > 1">
        <ul class="pagination">
          <li 
            v-for="page in totalPages" 
            :key="page"
            class="page-item"
            :class="{ active: currentPage === page }"
          >
            <button 
              class="page-link"
              @click="changePage(page)"
            >
              {{ page }}
            </button>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { API_BASE_URL } from '../../config';
import axios from 'axios';

const form = ref({
  name: '',
  category_id: '',
  price: 0,
  old_price: 0,
  brand: '',
  description: '',
  variants: [],
  images: [],
  main_image_index: 0
});

const isEditing = ref(false);
const editingId = ref(null);
const categories = ref([]);
const products = ref([]);
const currentPage = ref(1);
const totalPages = ref(1);
const filters = ref({
  search: '',
  category: null
});

// Загрузка категорий
const fetchCategories = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/admin/categories/tree`);
    categories.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке категорий:', error);
  }
};

// Загрузка товаров
const fetchProducts = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/admin/products`, {
      params: {
        page: currentPage.value,
        category_id: filters.value.category,
        search: filters.value.search
      }
    });
    products.value = response.data.items;
    totalPages.value = response.data.pages;
  } catch (error) {
    console.error('Ошибка при загрузке товаров:', error);
  }
};

// Управление вариантами
const addVariant = () => {
  form.value.variants.push({ name: '' });
};

const removeVariant = (index) => {
  form.value.variants.splice(index, 1);
};

// Управление изображениями
const handleImagesChange = async (event) => {
  const files = Array.from(event.target.files);
  for (const file of files) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('folder', 'products');

    try {
      const response = await axios.post(`${API_BASE_URL}/api/upload`, formData);
      form.value.images.push({
        url: response.data.file_path,
        file: file
      });
    } catch (error) {
      console.error('Ошибка при загрузке изображения:', error);
    }
  }
};

const setMainImage = (index) => {
  form.value.main_image_index = index;
};

const removeImage = (index) => {
  form.value.images.splice(index, 1);
  if (form.value.main_image_index >= form.value.images.length) {
    form.value.main_image_index = 0;
  }
};

// Отправка формы
const handleSubmit = async () => {
  try {
    const formData = new FormData();
    formData.append('name', form.value.name);
    formData.append('category_id', form.value.category_id);
    formData.append('price', form.value.price);
    formData.append('old_price', form.value.old_price);
    formData.append('brand', form.value.brand);
    formData.append('description', form.value.description);
    formData.append('variants', JSON.stringify(form.value.variants));
    formData.append('main_image_index', form.value.main_image_index);

    form.value.images.forEach((image, index) => {
      if (image.file) {
        formData.append('images', image.file);
      }
    });

    if (isEditing.value) {
      await axios.put(`${API_BASE_URL}/api/admin/products/${editingId.value}`, formData);
    } else {
      await axios.post(`${API_BASE_URL}/api/admin/products`, formData);
    }

    resetForm();
    await fetchProducts();
  } catch (error) {
    console.error('Ошибка при сохранении товара:', error);
  }
};

// Редактирование товара
const editProduct = async (product) => {
  isEditing.value = true;
  editingId.value = product.id;
  
  try {
    const response = await axios.get(`${API_BASE_URL}/api/admin/products/${product.id}`);
    const productData = response.data;
    
    form.value = {
      name: productData.name,
      category_id: productData.category_id,
      price: productData.price,
      old_price: productData.old_price,
      brand: productData.brand,
      description: productData.description,
      variants: productData.variants || [],
      images: productData.images.map(img => ({ url: img.url })),
      main_image_index: productData.images.findIndex(img => img.is_main)
    };
  } catch (error) {
    console.error('Ошибка при загрузке товара:', error);
  }
};

// Удаление товара
const deleteProduct = async (id) => {
  if (!confirm('Вы уверены, что хотите удалить этот товар?')) return;

  try {
    await axios.delete(`${API_BASE_URL}/api/admin/products/${id}`);
    await fetchProducts();
  } catch (error) {
    console.error('Ошибка при удалении товара:', error);
  }
};

// Сброс формы
const resetForm = () => {
  form.value = {
    name: '',
    category_id: '',
    price: 0,
    old_price: 0,
    brand: '',
    description: '',
    variants: [],
    images: [],
    main_image_index: 0
  };
  isEditing.value = false;
  editingId.value = null;
};

// Пагинация
const changePage = (page) => {
  currentPage.value = page;
  fetchProducts();
};

// Поиск
const handleSearch = () => {
  currentPage.value = 1;
  fetchProducts();
};

onMounted(() => {
  fetchCategories();
  fetchProducts();
});
</script>

<style scoped>
.admin-products {
  padding: 20px;
}

.product-form {
  background-color: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 30px;
}

.image-preview-item {
  position: relative;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  overflow: hidden;
}

.image-preview-item img {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.image-actions {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.7);
  padding: 8px;
  display: flex;
  gap: 8px;
}

.product-thumbnail {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 4px;
}

.variant-item {
  align-items: center;
}

.pagination {
  justify-content: center;
  margin-top: 20px;
}
</style>