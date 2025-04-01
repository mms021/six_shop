<template>
  <div class="admin-categories">
    <h2 class="press-start p-1">Управление категориями</h2>
    
    <!-- Форма создания/редактирования -->
    <div class="category-form mb-4">
      <h3>{{ isEditing ? 'Редактировать категорию' : 'Создать категорию' }}</h3>
      <form @submit.prevent="handleSubmit" class="p-3 border rounded">
        <div class="mb-3">
          <label class="form-label">Название категории</label>
          <input 
            v-model="form.name" 
            type="text" 
            class="form-control"
            required
          >
        </div>

        <div class="mb-3">
          <label class="form-label">Родительская категория</label>
          <select v-model="form.parent_id" class="form-select">
            <option :value="null">Нет родительской категории</option>
            <option 
              v-for="category in flatCategories" 
              :key="category.id"
              :value="category.id"
              :disabled="isEditing && category.id === editingId"
            >
              {{ category.name }}
            </option>
          </select>
        </div>

        <div class="mb-3">
          <label class="form-label">Изображение</label>
          <input 
            type="file" 
            class="form-control"
            @change="handleFileChange"
            accept="image/*"
          >
          <div v-if="form.image" class="mt-2">
            <img :src="form.image" alt="Preview" style="max-width: 200px">
          </div>
        </div>

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
    </div>

    <!-- Список категорий -->
    <div class="categories-list">
      <h3>Список категорий</h3>
      <div class="list-group">
        <template v-for="category in categories" :key="category.id">
          <!-- Основная категория -->
          <div class="list-group-item">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <img 
                  v-if="category.image" 
                  :src="category.image" 
                  alt="Category"
                  class="category-image me-2"
                >
                <strong>{{ category.name }}</strong>
              </div>
              <div class="btn-group">
                <button 
                  class="btn btn-sm btn-outline-primary"
                  @click="editCategory(category)"
                >
                  Редактировать
                </button>
                <button 
                  class="btn btn-sm btn-outline-danger"
                  @click="deleteCategory(category.id)"
                >
                  Удалить
                </button>
              </div>
            </div>
          </div>
          
          <!-- Подкатегории -->
          <div 
            v-for="child in category.children" 
            :key="child.id"
            class="list-group-item list-group-item-secondary ms-4"
          >
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <img 
                  v-if="child.image" 
                  :src="child.image" 
                  alt="Subcategory"
                  class="category-image me-2"
                >
                {{ child.name }}
              </div>
              <div class="btn-group">
                <button 
                  class="btn btn-sm btn-outline-primary"
                  @click="editCategory(child)"
                >
                  Редактировать
                </button>
                <button 
                  class="btn btn-sm btn-outline-danger"
                  @click="deleteCategory(child.id)"
                >
                  Удалить
                </button>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { API_BASE_URL } from '@/config';
import axios from 'axios';
import { useAuth } from '@/composables/useAuth';

const { user } = useAuth();
const categories = ref([]);
const isEditing = ref(false);
const editingId = ref(null);

const form = ref({
  name: '',
  parent_id: null,
  image: null
});

// Получаем плоский список категорий для селекта
const flatCategories = computed(() => {
  const flat = [];
  const flatten = (cats) => {
    cats.forEach(cat => {
      flat.push(cat);
      if (cat.children?.length) {
        flatten(cat.children);
      }
    });
  };
  flatten(categories.value);
  return flat;
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

// Обработка файла
const handleFileChange = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);
  formData.append('folder', 'categories');

  try {
    const response = await axios.post(`${API_BASE_URL}/api/upload`, formData);
    form.value.image = response.data.file_path;
  } catch (error) {
    console.error('Ошибка при загрузке файла:', error);
  }
};

// Создание/обновление категории
const handleSubmit = async () => {
  try {
    const formData = new FormData();
    formData.append('name', form.value.name);
    if (form.value.parent_id) {
      formData.append('parent_id', form.value.parent_id);
    }
    if (form.value.image) {
      formData.append('image', form.value.image);
    }

    if (isEditing.value) {
      await axios.put(`${API_BASE_URL}/api/admin/categories/${editingId.value}`, formData);
    } else {
      await axios.post(`${API_BASE_URL}/api/admin/categories`, formData);
    }

    // Очищаем форму и обновляем список
    resetForm();
    await fetchCategories();
  } catch (error) {
    console.error('Ошибка при сохранении категории:', error);
  }
};

// Редактирование категории
const editCategory = (category) => {
  isEditing.value = true;
  editingId.value = category.id;
  form.value = {
    name: category.name,
    parent_id: category.parent_id,
    image: category.image
  };
};

// Отмена редактирования
const cancelEdit = () => {
  isEditing.value = false;
  editingId.value = null;
  resetForm();
};

// Сброс формы
const resetForm = () => {
  form.value = {
    name: '',
    parent_id: null,
    image: null
  };
  isEditing.value = false;
  editingId.value = null;
};

// Удаление категории
const deleteCategory = async (id) => {
  if (!confirm('Вы уверены, что хотите удалить эту категорию?')) return;

  try {
    await axios.delete(`${API_BASE_URL}/api/admin/categories/${id}`);
    await fetchCategories();
  } catch (error) {
    console.error('Ошибка при удалении категории:', error);
  }
};

onMounted(() => {
  fetchCategories();
});
</script>

<style scoped>
.admin-categories {
  padding: 20px;
}

.category-image {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 4px;
}

.category-form {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 30px;
}

.list-group-item {
  border-left: 4px solid transparent;
}

.list-group-item-secondary {
  border-left-color: #6c757d;
}

.btn-group .btn {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}
</style>
