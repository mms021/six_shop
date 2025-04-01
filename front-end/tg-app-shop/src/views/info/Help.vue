<template>
  <div class="help-container">
    <div class="help-header">
      <h2 class="press-start text-center mb-4">Помощь</h2>
      <p class="text-muted text-center mb-5">Ответы на часто задаваемые вопросы</p>
    </div>

    <div class="faq-container">
      <div class="accordion" id="faqAccordion">
        <!-- Первый вопрос -->
        <div class="faq-item" :class="{ 'active': activeItem === 1 }">
          <div class="faq-header" @click="toggleItem(1)">
            <h3 class="faq-question">
              <i class="bi bi-newspaper me-2"></i>
              Где узнавать актуальную информацию о вашем ассортименте?
            </h3>
            <i class="bi" :class="activeItem === 1 ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
          </div>
          <transition name="fade">
            <div class="faq-answer" v-show="activeItem === 1">
              <p>
                Новинки публикуются каждый вечер в 6:00 на нашей страничке в Telegram. 
                Для получения актуальной информации:
              </p>
              <ul class="feature-list">
                <li>
                  <i class="bi bi-telegram text-primary"></i>
                  Подпишитесь на наш Telegram канал
                </li>
                <li>
                  <i class="bi bi-app-indicator"></i>
                  Откройте мини-приложение внутри канала
                </li>
                <li>
                  <i class="bi bi-cart-check"></i>
                  Добавляйте товары в корзину
                </li>
                <li>
                  <i class="bi bi-person-check"></i>
                  Личный менеджер свяжется с вами после модерации заказа
                </li>
              </ul>
            </div>
          </transition>
        </div>

        <!-- Второй вопрос -->
        <div class="faq-item" :class="{ 'active': activeItem === 2 }">
          <div class="faq-header" @click="toggleItem(2)">
            <h3 class="faq-question">
              <i class="bi bi-search me-2"></i>
              Что делать, если я не нашел нужную вещь?
            </h3>
            <i class="bi" :class="activeItem === 2 ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
          </div>
          <transition name="fade">
            <div class="faq-answer" v-show="activeItem === 2">
              <p>У нас есть несколько вариантов помощи в поиске:</p>
              <div class="help-options">
                <div class="help-option">
                  <i class="bi bi-person-workspace"></i>
                  <h4>Консьерж-сервис</h4>
                  <p>Заполните специальную форму, и наши специалисты помогут найти нужный товар</p>
                </div>
                <div class="help-option">
                  <i class="bi bi-chat-dots"></i>
                  <h4>Чат поддержки</h4>
                  <p>Опишите что ищете нашему менеджеру в Telegram</p>
                </div>
              </div>
            </div>
          </transition>
        </div>

        <!-- Третий вопрос -->
        <div class="faq-item" :class="{ 'active': activeItem === 3 }">
          <div class="faq-header" @click="toggleItem(3)">
            <h3 class="faq-question">
              <i class="bi bi-truck me-2"></i>
              Как происходит доставка?
            </h3>
            <i class="bi" :class="activeItem === 3 ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
          </div>
          <transition name="fade">
            <div class="faq-answer" v-show="activeItem === 3">
              <div class="delivery-info">
                <div class="delivery-option">
                  <i class="bi bi-geo-alt"></i>
                  <h4>Курьером</h4>
                  <p>Доставка по городу в течение 24 часов</p>
                </div>
                <div class="delivery-option">
                  <i class="bi bi-box-seam"></i>
                  <h4>Почтой</h4>
                  <p>Отправка в любой регион</p>
                </div>
                <div class="delivery-option">
                  <i class="bi bi-shop"></i>
                  <h4>Самовывоз</h4>
                  <p>Из нашего пункта выдачи</p>
                </div>
              </div>
            </div>
          </transition>
        </div>

        <!-- Четвертый вопрос -->
        <div class="faq-item" :class="{ 'active': activeItem === 4 }">
          <div class="faq-header" @click="toggleItem(4)">
            <h3 class="faq-question">
              <i class="bi bi-rulers me-2"></i>
              Есть ли примерка?
            </h3>
            <i class="bi" :class="activeItem === 4 ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
          </div>
          <transition name="fade">
            <div class="faq-answer" v-show="activeItem === 4">
              <p>Мы не предоставляем услугу примерки. Для правильного подбора размера:</p>
              <div class="help-options">
                <div class="help-option">
                  <i class="bi bi-people"></i>
                  <h4>Консультация менеджера</h4>
                  <p>Наши менеджеры отлично ориентируются в размерных сетках и часто знают точные замеры товаров</p>
                </div>
                <div class="help-option">
                  <i class="bi bi-rulers"></i>
                  <h4>Размерные сетки</h4>
                  <p>Вы можете ознакомиться с размерной сеткой на официальном сайте бренда</p>
                </div>
              </div>
            </div>
          </transition>
        </div>

        <!-- Пятый вопрос -->
        <div class="faq-item" :class="{ 'active': activeItem === 5 }">
          <div class="faq-header" @click="toggleItem(5)">
            <h3 class="faq-question">
              <i class="bi bi-arrow-return-left me-2"></i>
              Могу ли я вернуть товар?
            </h3>
            <i class="bi" :class="activeItem === 5 ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
          </div>
          <transition name="fade">
            <div class="faq-answer" v-show="activeItem === 5">
              <div class="alert alert-info">
                <i class="bi bi-info-circle-fill me-2"></i>
                Товары, приобретенные на платформе 6 o'clock, возврату и обмену не подлежат.
              </div>
            </div>
          </transition>
        </div>

        <!-- Шестой вопрос -->
        <div class="faq-item" :class="{ 'active': activeItem === 6 }">
          <div class="faq-header" @click="toggleItem(6)">
            <h3 class="faq-question">
              <i class="bi bi-truck me-2"></i>
              Где мой заказ? Сроки доставки
            </h3>
            <i class="bi" :class="activeItem === 6 ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
          </div>
          <transition name="fade">
            <div class="faq-answer" v-show="activeItem === 6">
              <div class="delivery-timeline">
                <div class="timeline-item">
                  <i class="bi bi-calendar-check"></i>
                  <h4>Сроки доставки</h4>
                  <p>От 7 до 20 дней из Европы (не включая доставку по России)</p>
                </div>
                <div class="timeline-item">
                  <i class="bi bi-geo-alt"></i>
                  <h4>Отслеживание</h4>
                  <p>Наши менеджеры оповестят вас о прибытии заказа на склад</p>
                </div>
              </div>
            </div>
          </transition>
        </div>

        <!-- Седьмой вопрос -->
        <div class="faq-item" :class="{ 'active': activeItem === 7 }">
          <div class="faq-header" @click="toggleItem(7)">
            <h3 class="faq-question">
              <i class="bi bi-patch-check me-2"></i>
              Аутентичность товаров
            </h3>
            <i class="bi" :class="activeItem === 7 ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
          </div>
          <transition name="fade">
            <div class="faq-answer" v-show="activeItem === 7">
              <div class="authenticity-info">
                <p><i class="bi bi-shield-check text-success me-2"></i>В каталогах представлены только оригинальные товары от брендов-производителей</p>
                <div class="additional-service">
                  <h4><i class="bi bi-plus-circle me-2"></i>Дополнительная услуга</h4>
                  <p>Возможен заказ сторонней аутентификации за дополнительную плату</p>
                </div>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </div>

    <!-- Дополнительная помощь -->
    <div class="additional-help mt-5">
      <h3 class="text-center mb-4">Нужна дополнительная помощь?</h3>
      <div class="contact-options">
        <a href="#" class="contact-option">
          <i class="bi bi-telegram"></i>
          <span>Написать в Telegram</span>
        </a>
        <a href="#" class="contact-option">
          <i class="bi bi-telephone"></i>
          <span>Позвонить нам</span>
        </a>
        <a href="#" class="contact-option">
          <i class="bi bi-envelope"></i>
          <span>Отправить email</span>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const activeItem = ref(null);

const toggleItem = (itemId) => {
  activeItem.value = activeItem.value === itemId ? null : itemId;
};
</script>

<style scoped>
.help-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.help-header {
  margin-bottom: 3rem;
}

.faq-item {
  background: white;
  border-radius: 12px;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
  transition: all 0.3s ease;
}

.faq-item.active {
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.faq-header {
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  background: linear-gradient(45deg, #f8f9fa, #ffffff);
}

.faq-question {
  font-size: 1.1rem;
  margin: 0;
  color: #333;
  display: flex;
  align-items: center;
}

.faq-answer {
  padding: 0 1.5rem 1.5rem;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 1rem 0;
}

.feature-list li {
  padding: 0.5rem 0;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.help-options, .delivery-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.help-option, .delivery-option {
  text-align: center;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.help-option:hover, .delivery-option:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.help-option i, .delivery-option i {
  font-size: 2rem;
  color: #4e73df;
  margin-bottom: 1rem;
}

.contact-options {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.contact-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem 1.5rem;
  background: white;
  border-radius: 8px;
  text-decoration: none;
  color: #333;
  transition: all 0.3s ease;
}

.contact-option:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Медиа-запросы */
@media (max-width: 768px) {
  .faq-question {
    font-size: 1rem;
  }
  
  .contact-options {
    flex-direction: column;
    gap: 1rem;
  }
  
  .contact-option {
    width: 100%;
    justify-content: center;
  }
}

.delivery-timeline {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin-top: 1rem;
}

.timeline-item {
  text-align: center;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.timeline-item i {
  font-size: 2rem;
  color: #4e73df;
  margin-bottom: 1rem;
}

.authenticity-info {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
}

.additional-service {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #dee2e6;
}

.alert {
  display: flex;
  align-items: center;
  margin: 0;
}

.alert i {
  font-size: 1.2rem;
}
</style>
