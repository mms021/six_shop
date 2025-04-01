<template>
  <div class="privacy-policy">
    <div class="container py-4">
      <h1 class="text-center mb-4">Политика конфиденциальности</h1>
      
      <div class="policy-section">
        <h2>1. Общие положения</h2>
        <p>Настоящая политика конфиденциальности описывает, как 6 O'clock Shop собирает, использует и защищает информацию, которую вы предоставляете при использовании нашего сервиса.</p>
      </div>

      <div class="policy-section">
        <h2>2. Собираемая информация</h2>
        <p>Мы собираем следующие типы информации:</p>
        <ul>
          <li>Идентификатор Telegram</li>
          <li>Имя пользователя</li>
          <li>Контактная информация (при оформлении заказа)</li>
          <li>История заказов</li>
          <li>Предпочтения и избранные товары</li>
        </ul>
      </div>

      <div class="policy-section">
        <h2>3. Использование информации</h2>
        <p>Собранная информация используется для:</p>
        <ul>
          <li>Обработки и доставки заказов</li>
          <li>Улучшения качества обслуживания</li>
          <li>Персонализации предложений</li>
          <li>Технической поддержки</li>
          <li>Информирования о статусе заказа</li>
        </ul>
      </div>

      <div class="policy-section">
        <h2>4. Защита информации</h2>
        <p>Мы принимаем следующие меры для защиты ваших данных:</p>
        <ul>
          <li>Шифрование данных при передаче</li>
          <li>Ограниченный доступ к персональным данным</li>
          <li>Регулярное обновление систем безопасности</li>
          <li>Мониторинг и аудит систем безопасности</li>
        </ul>
      </div>

      <div class="policy-section">
        <h2>5. Права пользователя</h2>
        <p>Вы имеете право:</p>
        <ul>
          <li>Получить доступ к своим данным</li>
          <li>Исправить неточные данные</li>
          <li>Удалить свои данные</li>
          <li>Ограничить обработку данных</li>
          <li>Получить копию своих данных</li>
        </ul>
      </div>

      <div class="policy-section">
        <h2>6. Контакты</h2>
        <p>По вопросам, связанным с обработкой персональных данных, обращайтесь:</p>
        <div class="contact-info">
          <p><i class="bi bi-envelope"></i> {{ supportEmail }}</p>
          <p><i class="bi bi-telephone"></i> {{ supportPhone }}</p>
          <p><i class="bi bi-clock"></i> {{ workTime }}</p>
        </div>
      </div>

      <div class="policy-section">
        <h2>7. Изменения политики</h2>
        <p>Мы оставляем за собой право вносить изменения в данную политику конфиденциальности. Все изменения будут опубликованы на этой странице.</p>
        <p class="last-updated">Последнее обновление: {{ lastUpdated }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const supportEmail = ref(import.meta.env.VITE_SUPPORT_EMAIL || 'support@6oclock.shop');
const supportPhone = ref(import.meta.env.VITE_SUPPORT_PHONE || '+7 (XXX) XXX-XX-XX');
const workTime = ref(import.meta.env.VITE_WORK_TIME || '24/7');
const lastUpdated = ref('15 марта 2024');
</script>

<style scoped>
.privacy-policy {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.policy-section {
  background-color: #fff;
  border-radius: 8px;
  padding: 2rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

h1 {
  color: #2c3e50;
  font-weight: 600;
  margin-bottom: 2rem;
}

h2 {
  color: #3498db;
  font-size: 1.5rem;
  margin-bottom: 1rem;
  font-weight: 500;
}

p {
  color: #4a5568;
  line-height: 1.6;
  margin-bottom: 1rem;
}

ul {
  list-style-type: none;
  padding-left: 0;
}

li {
  color: #4a5568;
  margin-bottom: 0.5rem;
  padding-left: 1.5rem;
  position: relative;
}

li:before {
  content: "•";
  color: #3498db;
  font-weight: bold;
  position: absolute;
  left: 0;
}

.contact-info {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 6px;
  margin-top: 1rem;
}

.contact-info p {
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.contact-info i {
  color: #3498db;
}

.last-updated {
  color: #718096;
  font-style: italic;
  margin-top: 1rem;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .policy-section {
    padding: 1.5rem;
  }

  h1 {
    font-size: 1.8rem;
  }

  h2 {
    font-size: 1.3rem;
  }
}
</style>
