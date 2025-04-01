<template>
  <div class="terms-of-service">
    <div class="container py-4">
      <h1 class="text-center mb-4">Условия использования</h1>
      
      <div class="terms-section">
        <h2>1. Общие положения</h2>
        <p>Настоящие условия использования регулируют отношения между 6 O'clock Shop (далее - "Сервис") и пользователями. Используя наш сервис, вы соглашаетесь с данными условиями.</p>
      </div>

      <div class="terms-section">
        <h2>2. Регистрация и использование</h2>
        <p>При использовании сервиса вы соглашаетесь:</p>
        <ul>
          <li>Предоставлять достоверную информацию при регистрации</li>
          <li>Использовать сервис только в законных целях</li>
          <li>Не нарушать работу сервиса</li>
          <li>Не создавать множественные аккаунты</li>
          <li>Не использовать автоматизированные системы</li>
        </ul>
      </div>

      <div class="terms-section">
        <h2>3. Заказы и оплата</h2>
        <p>Правила оформления и оплаты заказов:</p>
        <ul>
          <li>Цены указаны в рублях с учетом НДС</li>
          <li>Оплата производится через Telegram</li>
          <li>Заказ считается принятым после подтверждения оплаты</li>
          <li>Возврат средств осуществляется согласно законодательству РФ</li>
          <li>Доставка осуществляется по указанному адресу</li>
        </ul>
      </div>

      <div class="terms-section">
        <h2>4. Интеллектуальная собственность</h2>
        <p>Все материалы сервиса защищены:</p>
        <ul>
          <li>Товарные знаки и логотипы являются собственностью сервиса</li>
          <li>Запрещено копирование и распространение контента</li>
          <li>Фотографии товаров защищены авторским правом</li>
          <li>Нарушение прав преследуется по закону</li>
        </ul>
      </div>

      <div class="terms-section">
        <h2>5. Ответственность</h2>
        <p>Ограничение ответственности:</p>
        <ul>
          <li>Сервис не несет ответственности за действия третьих лиц</li>
          <li>Пользователь несет ответственность за свои действия</li>
          <li>Сервис может быть временно недоступен</li>
          <li>Товары могут отличаться от изображений</li>
        </ul>
      </div>

      <div class="terms-section">
        <h2>6. Возврат и обмен</h2>
        <p>Правила возврата товаров:</p>
        <ul>
          <li>Возврат возможен в течение 14 дней</li>
          <li>Товар должен быть в оригинальной упаковке</li>
          <li>Возврат средств в течение 10 рабочих дней</li>
          <li>Доставка возврата оплачивается покупателем</li>
        </ul>
      </div>

      <div class="terms-section">
        <h2>7. Контактная информация</h2>
        <p>По всем вопросам обращайтесь:</p>
        <div class="contact-info">
          <p><i class="bi bi-envelope"></i> {{ supportEmail }}</p>
          <p><i class="bi bi-telephone"></i> {{ supportPhone }}</p>
          <p><i class="bi bi-clock"></i> {{ workTime }}</p>
          <p><i class="bi bi-geo-alt"></i> {{ supportAddress }}</p>
        </div>
      </div>

      <div class="terms-section">
        <h2>8. Изменения условий</h2>
        <p>Мы оставляем за собой право изменять данные условия использования. Актуальная версия всегда доступна на этой странице.</p>
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
const supportAddress = ref(import.meta.env.VITE_SUPPORT_ADDRESS || 'г. Москва');
const lastUpdated = ref('15 марта 2024');
</script>

<style scoped>
.terms-of-service {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.terms-section {
  background-color: #fff;
  border-radius: 8px;
  padding: 2rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  transition: transform 0.2s ease;
}

.terms-section:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

h1 {
  color: #2c3e50;
  font-weight: 600;
  margin-bottom: 2rem;
}

h2 {
  color: #2c3e50;
  font-size: 1.5rem;
  margin-bottom: 1rem;
  font-weight: 500;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 0.5rem;
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
  content: "→";
  color: #3498db;
  position: absolute;
  left: 0;
}

.contact-info {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 6px;
  margin-top: 1rem;
  border-left: 4px solid #3498db;
}

.contact-info p {
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.contact-info i {
  color: #3498db;
  font-size: 1.1rem;
}

.last-updated {
  color: #718096;
  font-style: italic;
  margin-top: 1rem;
  font-size: 0.9rem;
  text-align: right;
}

@media (max-width: 768px) {
  .terms-section {
    padding: 1.5rem;
  }

  h1 {
    font-size: 1.8rem;
  }

  h2 {
    font-size: 1.3rem;
  }

  .contact-info {
    padding: 1rem;
  }
}
</style>
