<template>
  <div class="concierge-container">
    <div class="concierge-content">
      <div class="concierge-header text-center">
        <h1 class="press-start mb-4">Консьерж-сервис</h1>
        <div class="subtitle mb-5">
          <p class="lead">
            Не нашли подходящий товар? <br />
            Воспользуйтесь нашим консьерж-сервисом, и мы подберем для вас товар из любой точки мира.
          </p>
        </div>
      </div>

      <div class="form-container">
        <form @submit.prevent="submitRequest" class="concierge-form">
          <!-- Статус отправки -->
          <div v-if="status" :class="['alert', status.success ? 'alert-success' : 'alert-danger']">
            {{ status.message }}
          </div>

          <!-- Имя -->
          <div class="form-group">
            <label for="name">
              <i class="bi bi-person"></i> Ваше имя
            </label>
            <input 
              type="text" 
              id="name" 
              v-model="form.name" 
              :class="['form-control', {'is-invalid': errors.name}]"
              required
            />
            <div class="invalid-feedback" v-if="errors.name">
              {{ errors.name }}
            </div>
          </div>

          <!-- Контакт -->
          <div class="form-group">
            <label for="contact">
              <i class="bi bi-telephone"></i> Контакт для связи
            </label>
            <input 
              type="text" 
              id="contact" 
              v-model="form.contact" 
              :class="['form-control', {'is-invalid': errors.contact}]"
              required
            />
            <div class="invalid-feedback" v-if="errors.contact">
              {{ errors.contact }}
            </div>
          </div>

          <!-- Ссылка на товар -->
          <div class="form-group">
            <label for="productLink">
              <i class="bi bi-link-45deg"></i> Ссылка на товар (если есть)
            </label>
            <input 
              type="url" 
              id="productLink" 
              v-model="form.productLink" 
              :class="['form-control', {'is-invalid': errors.productLink}]"
            />
            <div class="invalid-feedback" v-if="errors.productLink">
              {{ errors.productLink }}
            </div>
          </div>

          <!-- Детали запроса -->
          <div class="form-group">
            <label for="details">
              <i class="bi bi-chat-text"></i> Опишите, что вы ищете
            </label>
            <textarea 
              id="details" 
              v-model="form.details" 
              :class="['form-control', {'is-invalid': errors.details}]"
              rows="5"
              required
            ></textarea>
            <div class="invalid-feedback" v-if="errors.details">
              {{ errors.details }}
            </div>
          </div>

          <!-- Кнопка отправки -->
          <button 
            type="submit" 
            class="btn btn-primary w-100"
            :disabled="loading"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            {{ loading ? 'Отправка...' : 'Отправить запрос' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import axios from 'axios';
import { API_BASE_URL } from '@/config';

const form = reactive({
  name: '',
  contact: '',
  productLink: '',
  details: ''
});

const errors = reactive({});
const loading = ref(false);
const status = ref(null);

const validateForm = () => {
  errors.name = !form.name ? 'Пожалуйста, укажите ваше имя' : '';
  errors.contact = !form.contact ? 'Пожалуйста, укажите контакт для связи' : '';
  errors.details = !form.details ? 'Пожалуйста, опишите ваш запрос' : '';
  
  if (form.productLink && !form.productLink.startsWith('http')) {
    errors.productLink = 'Пожалуйста, укажите корректную ссылку';
  }

  return !Object.values(errors).some(error => error);
};

const submitRequest = async () => {
  if (!validateForm()) return;
  
  loading.value = true;
  status.value = null;

  try {
    const formData = new FormData();
    formData.append('name', form.name);
    formData.append('contact', form.contact);
    formData.append('product_link', form.productLink);
    formData.append('details', form.details);

    const response = await axios.post(`${API_BASE_URL}/api/concierge/request`, formData);
    
    status.value = {
      success: true,
      message: response.data.message
    };

    // Очищаем форму при успешной отправке
    form.name = '';
    form.contact = '';
    form.productLink = '';
    form.details = '';
    
  } catch (error) {
    status.value = {
      success: false,
      message: 'Произошла ошибка при отправке запроса. Пожалуйста, попробуйте позже.'
    };
    console.error('Error:', error);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.concierge-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.concierge-content {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}

.concierge-header {
  margin-bottom: 2rem;
}

.form-container {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.concierge-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #495057;
}

.form-group label i {
  color: #6c757d;
}

.form-control {
  border: 2px solid #e9ecef;
  border-radius: 8px;
  padding: 0.75rem;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: #4e73df;
  box-shadow: 0 0 0 0.2rem rgba(78, 115, 223, 0.1);
}

.btn-primary {
  background: linear-gradient(45deg, #4e73df, #6f42c1);
  border: none;
  padding: 1rem;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(78, 115, 223, 0.3);
}

.btn-primary:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.alert {
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

/* Анимации */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.alert {
  animation: fadeIn 0.3s ease;
}

/* Медиа-запросы */
@media (max-width: 768px) {
  .concierge-container {
    padding: 1rem;
  }
  
  .form-container {
    padding: 1.5rem;
  }
}
</style>

